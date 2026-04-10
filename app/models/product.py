from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(150), unique=True, nullable=False)
    categorie = Column(String(100))
    description = Column(Text)
    unite = Column(String(20), default="kg")
