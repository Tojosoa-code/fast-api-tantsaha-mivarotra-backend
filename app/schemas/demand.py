from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


class DemandBase(BaseModel):
    product_id: int
    quantite: Decimal = Field(..., gt=0)
    budget_max: Optional[Decimal] = None
    latitude: float
    longitude: float
    region: str
    date_souhaitee: Optional[date] = None


class DemandCreate(DemandBase):
    pass


class DemandRead(DemandBase):
    id: int
    acheteur_id: int
    statut: str
    created_at: datetime

    class Config:
        from_attributes = True
