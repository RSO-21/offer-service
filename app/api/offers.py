from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional

import grpc
from ..grpc_generated import partner_pb2, partner_pb2_grpc

from ..db import get_db, get_db_session
from .. import models, schemas

from ..config import settings

router = APIRouter(
    prefix="/offers",
    tags=["offers"],
)

def get_tenant_id(x_tenant_id: Optional[str] = Header(None)) -> str:
    """Extract tenant ID from header, default to public"""
    return x_tenant_id or "public"

def get_db_with_schema(tenant_id: str = Depends(get_tenant_id)):
    with get_db_session(schema=tenant_id) as db:
        yield db


@router.get("/", response_model=list[schemas.OfferRead])
def list_offers(db: Session = Depends(get_db_with_schema)):
    return db.query(models.Offer).all()


@router.post("/", response_model=schemas.OfferRead, status_code=201)
def create_offer(offer: schemas.OfferBase, db: Session = Depends(get_db_with_schema), tenant_id: str = Depends(get_tenant_id)):
    # 1) preveri partnerja preko gRPC
    partner = get_partner_via_grpc(offer.partner_id, tenant_id)
    if partner is None or partner.active is False:
        raise HTTPException(status_code=400, detail="Invalid or inactive partner")

    # 2) shrani offer v DB
    db_offer = models.Offer(**offer.dict())
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


@router.get("/{offer_id}", response_model=schemas.OfferRead)
def get_offer(offer_id: int, db: Session = Depends(get_db_with_schema)):
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.put("/{offer_id}", response_model=schemas.OfferRead)
def update_offer(offer_id: int, offer_update: schemas.OfferUpdate, db: Session = Depends(get_db_with_schema)):
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    update_data = offer_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(offer, key, value)

    db.commit()
    db.refresh(offer)
    return offer

@router.delete("/{offer_id}", status_code=204)
def delete_offer(offer_id: int, db: Session = Depends(get_db_with_schema)):
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    db.delete(offer)
    db.commit()
    return None

@router.get(
    "/by-partner/{partner_id}",
    response_model=list[schemas.OfferRead]
)
def list_offers_by_partner(
    partner_id: str,
    db: Session = Depends(get_db_with_schema),
):
    offers = (
        db.query(models.Offer)
        .filter(models.Offer.partner_id == partner_id)
        .all()
    )

    return offers

@router.post(
    "/bulk",
    response_model=list[schemas.OfferRead]
)
def get_offers_bulk(
    payload: schemas.OfferBulkRequest,
    db: Session = Depends(get_db_with_schema),
):
    if not payload.ids:
        return []

    offers = (
        db.query(models.Offer)
        .filter(models.Offer.id.in_(payload.ids))
        .all()
    )

    return offers


def get_partner_via_grpc(partner_id: int, tenant_id: Optional[str] = None):
    target = f"{settings.partner_grpc_host}:{settings.partner_grpc_port}"
    metadata = [("x-tenant-id", (tenant_id or "public"))]
    with grpc.insecure_channel(target) as channel:
        stub = partner_pb2_grpc.PartnerServiceStub(channel)
        request = partner_pb2.GetPartnerRequest(id=partner_id)
        try:
            response = stub.GetPartner(request, metadata=metadata)
            return response
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise