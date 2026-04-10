from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class MatchRead(BaseModel):
    id: int
    offer_id: int
    demand_id: int
    score: Decimal
    distance_km: Decimal
    created_at: datetime

    class Config:
        from_attributes = True
