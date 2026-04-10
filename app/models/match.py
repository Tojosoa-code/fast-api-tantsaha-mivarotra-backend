from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    demand_id = Column(Integer, ForeignKey("demands.id"))
    score = Column(DECIMAL(5, 2))
    distance_km = Column(DECIMAL(8, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
