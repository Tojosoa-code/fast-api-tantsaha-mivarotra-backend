from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


class ProductBrief(BaseModel):
    id: int
    nom: str
    categorie: str
    description: str
    unite: str

    class Config:
        from_attributes = True


class UserBrief(BaseModel):
    id: int
    prenom: Optional[str] = None
    nom: Optional[str] = None
    region: Optional[str] = None

    class Config:
        from_attributes = True


class OfferBase(BaseModel):
    product_id: int
    quantite: Decimal = Field(..., gt=0)
    prix_unitaire: Decimal = Field(..., gt=0)
    latitude: float
    longitude: float
    region: str
    date_dispo_debut: Optional[date] = None
    date_dispo_fin: Optional[date] = None


class OfferCreate(OfferBase):
    pass


class OfferRead(OfferBase):
    id: int
    producteur_id: int
    statut: str
    created_at: datetime

    # ✅ Champs imbriqués (seront remplis grâce à joinedload)
    product: Optional[ProductBrief] = None
    producteur: Optional[UserBrief] = None

    class Config:
        from_attributes = True
