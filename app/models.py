from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from .db import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(Integer, nullable=False)  # brez FK

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    price_original = Column(Float, nullable=False)
    price_discounted = Column(Float, nullable=False)

    quantity_total = Column(Integer, nullable=False)
    quantity_available = Column(Integer, nullable=False)

    pickup_from = Column(DateTime, nullable=False)
    pickup_until = Column(DateTime, nullable=False)

    status = Column(String, default="ACTIVE")
    tenant_id = Column(String, nullable=True)
