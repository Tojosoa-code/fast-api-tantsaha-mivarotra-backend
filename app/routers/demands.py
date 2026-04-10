from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.demand import Demand
from app.schemas.demand import DemandCreate, DemandRead
from app.crud.base import CRUDBase

router = APIRouter()
crud_demand = CRUDBase(Demand)


@router.post("/", response_model=DemandRead)
def create_demand(demand_in: DemandCreate, db: Session = Depends(get_db)):
    return crud_demand.create(db, demand_in.model_dump())


@router.get("/", response_model=list[DemandRead])
def get_demands(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_demand.get_multi(db, skip, limit)
