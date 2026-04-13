# app/routers/demands.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc
from typing import Optional
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

    demand = crud_demand.create(db, demand_dict)

    return (
        db.query(Demand)
        .options(joinedload(Demand.product), joinedload(Demand.acheteur))
        .filter(Demand.id == demand.id)
        .first()
    )


@router.get("/")
def get_demands(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    region: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
):
    query = db.query(Demand).options(
        joinedload(Demand.product), joinedload(Demand.acheteur)
    )

    # ✅ FILTRE REGION
    if region:
        query = query.filter(Demand.region == region)

    # ✅ TRI DYNAMIQUE
    sort_column_map = {
        "created_at": Demand.created_at,
        "budget_max": Demand.budget_max,
        "quantite": Demand.quantite,
    }

    sort_column = sort_column_map.get(sort_by, Demand.created_at)

    if sort_order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    # ✅ TOTAL AVANT PAGINATION
    total = query.count()

    # ✅ PAGINATION
    demands = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": demands,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.get("/{demand_id}", response_model=DemandRead)
def get_demand(demand_id: int, db: Session = Depends(get_db)):
    demand = (
        db.query(Demand)
        .options(joinedload(Demand.product), joinedload(Demand.acheteur))
        .filter(Demand.id == demand_id)
        .first()
    )
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
    crud_demand.update(db, demand_id, demand_dict)

    return (
        db.query(Demand)
        .options(joinedload(Demand.acheteur), joinedload(Demand.product))
        .filter(Demand.id == demand_id)
        .first()
    )


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
