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


@router.get("/{demand_id}", response_model=DemandRead)
def get_demand(demand_id: int, db: Session = Depends(get_db)):
    demand = crud_demand.get(db, demand_id)
    if not demand:
        raise HTTPException(status_code=404, detail="Demande non trouvée")
    return demand


@router.put("/{demand_id}", response_model=DemandRead)
def update_demand(
    demand_id: int,
    demand_in: DemandCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    demand = crud_demand.get(db, demand_id)
    if not demand:
        raise HTTPException(status_code=404, detail="Demande non trouvée")
    if demand.acheteur_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous ne pouvez modifier que vos propres demandes"
        )

    demand_dict = demand_in.model_dump(exclude_unset=True)
    return crud_demand.update(db, demand_id, demand_dict)


@router.delete("/{demand_id}")
def delete_demand(
    demand_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    demand = crud_demand.get(db, demand_id)
    if not demand:
        raise HTTPException(status_code=404, detail="Demande non trouvée")
    if demand.acheteur_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous ne pouvez supprimer que vos propres demandes"
        )

    crud_demand.delete(db, demand_id)
    return {"message": "Demande supprimée avec succès"}
