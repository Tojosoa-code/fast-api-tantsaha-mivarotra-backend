from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


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

    class Config:
        from_attributes = True
