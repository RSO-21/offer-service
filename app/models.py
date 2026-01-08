from sqlalchemy import Column, Integer, String, Boolean, Float, Date, text
from .db import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, autoincrement=True, server_default=text("nextval('offers_id_seq')"))
    partner_id = Column(String(36), primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    price_original = Column(Float, nullable=False)
    price_discounted = Column(Float, nullable=False)

    expiry_date = Column(Date, nullable=False)

    status = Column(String, default="ACTIVE")
    tenant_id = Column(String, nullable=True)
