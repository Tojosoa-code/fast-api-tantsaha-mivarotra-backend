from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
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

    return crud_offer.create(db, offer_dict)


@router.get("/", response_model=list[OfferRead])
def get_offers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_offer.get_multi(db, skip, limit)


@router.get("/{offer_id}", response_model=OfferRead)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = crud_offer.get(db, offer_id)
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
    return crud_offer.update(db, offer_id, offer_dict)


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
