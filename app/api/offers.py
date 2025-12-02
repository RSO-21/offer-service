from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/offers",
    tags=["offers"],
)


@router.get("/", response_model=list[schemas.OfferRead])
def list_offers(db: Session = Depends(get_db)):
    return db.query(models.Offer).all()


@router.post("/", response_model=schemas.OfferRead, status_code=201)
def create_offer(offer: schemas.OfferCreate, db: Session = Depends(get_db)):
    # Optionally: Validate partner ID by calling Partner Service (in next step)
    
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
