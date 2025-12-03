from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import grpc
from ..grpc_generated import partner_pb2, partner_pb2_grpc

from ..db import get_db
from .. import models, schemas

from ..config import settings

router = APIRouter(
    prefix="/offers",
    tags=["offers"],
)


@router.get("/", response_model=list[schemas.OfferRead])
def list_offers(db: Session = Depends(get_db)):
    return db.query(models.Offer).all()


@router.post("/", response_model=schemas.OfferRead, status_code=201)
def create_offer(offer: schemas.OfferCreate, db: Session = Depends(get_db)):
    # 1) preveri partnerja preko gRPC
    partner = get_partner_via_grpc(offer.partner_id)
    if partner is None or partner.active is False:
        raise HTTPException(status_code=400, detail="Invalid or inactive partner")

    # 2) shrani offer v DB
    db_offer = models.Offer(**offer.dict())
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


@router.get("/{offer_id}", response_model=schemas.OfferRead)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.put("/{offer_id}", response_model=schemas.OfferRead)
def update_offer(offer_id: int, offer_update: schemas.OfferUpdate, db: Session = Depends(get_db)):
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
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    db.delete(offer)
    db.commit()
    return None

def get_partner_via_grpc(partner_id: int):
    target = f"{settings.partner_grpc_host}:{settings.partner_grpc_port}"
    with grpc.insecure_channel(target) as channel:
        stub = partner_pb2_grpc.PartnerServiceStub(channel)
        request = partner_pb2.GetPartnerRequest(id=partner_id)
        try:
            response = stub.GetPartner(request)
            return response
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise