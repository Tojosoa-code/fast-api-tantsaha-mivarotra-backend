from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.offer import Offer
from app.models.demand import Demand
from app.schemas.offer import OfferRead
from app.schemas.demand import DemandRead

router = APIRouter()


@router.get("/me/offers", response_model=list[OfferRead])
def get_my_offers(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Retourne toutes les offres du producteur connecté"""
    offers = db.query(Offer).filter(Offer.producteur_id == current_user.id).all()
    return offers


@router.get("/me/demands", response_model=list[DemandRead])
def get_my_demands(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Retourne toutes les demandes de l'acheteur connecté"""
    demands = db.query(Demand).filter(Demand.acheteur_id == current_user.id).all()
    return demands
