from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OfferBase(BaseModel):
    partner_id: str
    title: str
    description: Optional[str] = None
    price_original: float
    price_discounted: float
    quantity_total: int
    quantity_available: int
    pickup_from: datetime
    pickup_until: datetime
    status: Optional[str] = "ACTIVE"
    tenant_id: Optional[str] = None


class OfferCreate(OfferBase):
    pass


class OfferUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price_original: Optional[float] = None
    price_discounted: Optional[float] = None
    quantity_total: Optional[int] = None
    quantity_available: Optional[int] = None
    pickup_from: Optional[datetime] = None
    pickup_until: Optional[datetime] = None
    status: Optional[str] = None
    tenant_id: Optional[str] = None


class OfferRead(OfferBase):
    id: int

    model_config = {
        "from_attributes": True
    }
