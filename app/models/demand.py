from sqlalchemy import Column, Integer, Float, DateTime, Date, String, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from app.core.database import Base

class Demand(Base):
    __tablename__ = "demands"

    id = Column(Integer, primary_key=True, index=True)
    acheteur_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantite = Column(DECIMAL(10, 2), nullable=False)
    budget_max = Column(DECIMAL(10, 2))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    region = Column(String(100), nullable=False)
    date_souhaitee = Column(Date)
    statut = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
