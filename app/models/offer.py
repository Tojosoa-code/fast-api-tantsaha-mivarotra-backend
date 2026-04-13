from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    Date,
    String,
    ForeignKey,
    DECIMAL,
)
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    producteur_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantite = Column(DECIMAL(10, 2), nullable=False)
    prix_unitaire = Column(DECIMAL(10, 2), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    region = Column(String(100), nullable=False)  # multi-régions
    date_dispo_debut = Column(Date)
    date_dispo_fin = Column(Date)
    statut = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    producteur = relationship("User")
    product = relationship("Product")
