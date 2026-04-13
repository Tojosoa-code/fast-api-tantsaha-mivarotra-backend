from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user, get_optional_current_user
from app.models.offer import Offer
from app.models.user import User
from app.schemas.offer import OfferCreate, OfferRead
from app.crud.base import CRUDBase

router = APIRouter()
crud_offer = CRUDBase(Offer)


@router.post("/", response_model=OfferRead)
def create_offer(
    offer_in: OfferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "producteur":
        raise HTTPException(
            status_code=403, detail="Seuls les producteurs peuvent créer des offres"
        )

    offer_dict = offer_in.model_dump()
    offer_dict["producteur_id"] = current_user.id
    offer_dict["region"] = current_user.region

    offer = crud_offer.create(db, offer_dict)

    return (
        db.query(Offer)
        .options(joinedload(Offer.product), joinedload(Offer.producteur))
        .filter(Offer.id == offer.id)
        .first()
    )


@router.get("/")
def get_offers(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),  # ✅ Optionnel
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    exclude_current_user: bool = Query(
        False, description="Exclure mes propres offres"
    ),  # ✅ NOUVEAU
    region: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
):
    query = db.query(Offer).options(
        joinedload(Offer.product), joinedload(Offer.producteur)
    )

    # ✅ NOUVEAU : Exclure les offres de l'utilisateur connecté
    if exclude_current_user and current_user:
        query = query.filter(Offer.producteur_id != current_user.id)

    # ✅ FILTRE REGION
    if region:
        query = query.filter(Offer.region == region)

    # ✅ TRI DYNAMIQUE
    sort_column_map = {
        "created_at": Offer.created_at,
        "prix_unitaire": Offer.prix_unitaire,
        "quantite": Offer.quantite,
    }

    sort_column = sort_column_map.get(sort_by, Offer.created_at)

    if sort_order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    # ✅ TOTAL APRÈS FILTRAGE, AVANT PAGINATION
    total = query.count()

    # ✅ PAGINATION
    offers = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": offers,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if total > 0 else 1,
    }


@router.get("/{offer_id}", response_model=OfferRead)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = (
        db.query(Offer)
        .options(joinedload(Offer.product), joinedload(Offer.producteur))
        .filter(Offer.id == offer_id)
        .first()
    )
    if not offer:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    return offer


@router.put("/{offer_id}", response_model=OfferRead)
def update_offer(
    offer_id: int,
    offer_in: OfferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    offer = crud_offer.get(db, offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    if offer.producteur_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous ne pouvez modifier que vos propres offres"
        )

    offer_dict = offer_in.model_dump(exclude_unset=True)
    crud_offer.update(db, offer_id, offer_dict)

    return (
        db.query(Offer)
        .options(joinedload(Offer.product), joinedload(Offer.producteur))
        .filter(Offer.id == offer_id)
        .first()
    )


@router.delete("/{offer_id}")
def delete_offer(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    offer = crud_offer.get(db, offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    if offer.producteur_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Vous ne pouvez supprimer que vos propres offres"
        )

    crud_offer.delete(db, offer_id)
    return {"message": "Offre supprimée avec succès"}
