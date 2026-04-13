from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(150), unique=True, nullable=False)
    categorie = Column(String(100))
    description = Column(Text)
    unite = Column(String(20), default="kg")

    offers = relationship("Offer", back_populates="product")
    demands = relationship("Demand", back_populates="product")
