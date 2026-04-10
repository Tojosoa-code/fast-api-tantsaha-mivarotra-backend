from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.offer import Offer
from app.schemas.offer import OfferCreate, OfferRead
from app.crud.base import CRUDBase

router = APIRouter()
crud_offer = CRUDBase(Offer)

@router.post("/", response_model=OfferRead)
def create_offer(offer_in: OfferCreate, db: Session = Depends(get_db)):
    return crud_offer.create(db, offer_in.model_dump())

@router.get("/", response_model=list[OfferRead])
def get_offers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_offer.get_multi(db, skip, limit)
