from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductRead
from app.crud.base import CRUDBase
from app.algorithms.trie import product_trie

router = APIRouter()
crud_product = CRUDBase(Product)


@router.post("/", response_model=ProductRead)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),  # optionnel : on peut restreindre à admin plus tard
):
    """Création d'un produit + insertion automatique dans le Trie"""
    product = crud_product.create(db, product_in.model_dump())
    product_trie.insert(product.nom, product.id)
    return product


@router.get("/", response_model=list[ProductRead])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Liste de tous les produits"""
    return crud_product.get_multi(db, skip, limit)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud_product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mise à jour d'un produit"""
    product = crud_product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    # Mise à jour dans la base
    updated_product = crud_product.update(
        db, product_id, product_in.model_dump(exclude_unset=True)
    )

    # Mise à jour du Trie (on ré-insère le nouveau nom)
    product_trie.insert(updated_product.nom, updated_product.id)

    return updated_product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Suppression d'un produit"""
    product = crud_product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    crud_product.delete(db, product_id)
    return {"message": f"Produit {product_id} supprimé avec succès"}
