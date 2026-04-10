from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead
from app.crud.base import CRUDBase

router = APIRouter()
crud_product = CRUDBase(Product)

@router.post("/", response_model=ProductRead)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create(db, product_in.model_dump())

@router.get("/", response_model=list[ProductRead])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_product.get_multi(db, skip, limit)
