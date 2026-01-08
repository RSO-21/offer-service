from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional


class OfferBase(BaseModel):
    partner_id: str
    title: str
    description: Optional[str] = None
    price_original: float
    price_discounted: float
    expiry_date: date
    status: Optional[str] = "ACTIVE"
    tenant_id: Optional[str] = None


class OfferUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price_original: Optional[float] = None
    price_discounted: Optional[float] = None
    expiry_date: Optional[date] = None
    status: Optional[str] = None
    tenant_id: Optional[str] = None


class OfferRead(OfferBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class OfferBulkRequest(BaseModel):
    ids: List[int]