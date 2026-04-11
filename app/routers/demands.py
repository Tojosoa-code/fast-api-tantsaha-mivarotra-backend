from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.demand import Demand
from app.models.user import User
from app.schemas.demand import DemandCreate, DemandRead
from app.crud.base import CRUDBase

router = APIRouter()
crud_demand = CRUDBase(Demand)


@router.post("/", response_model=DemandRead)
def create_demand(
    demand_in: DemandCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "acheteur":
        raise HTTPException(
            status_code=403, detail="Seuls les acheteurs peuvent créer des demandes"
        )

    demand_dict = demand_in.model_dump()
    demand_dict["acheteur_id"] = current_user.id
    demand_dict["region"] = current_user.region

    return crud_demand.create(db, demand_dict)


@router.get("/", response_model=list[DemandRead])
def get_demands(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_demand.get_multi(db, skip, limit)
