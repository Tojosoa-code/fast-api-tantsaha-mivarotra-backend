from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.algorithms.matching import greedy_matching
from app.algorithms.routing import nearest_neighbor_tsp
from app.algorithms.trie import product_trie
from app.models.product import Product

router = APIRouter()


@router.get("/search")
def search_products(prefix: str, db: Session = Depends(get_db)):
    """Recherche rapide avec Trie"""
    product_ids = product_trie.search_prefix(prefix)
    if not product_ids:
        return []
    return db.query(Product).filter(Product.id.in_(product_ids)).all()


@router.post("/match")
def find_matches(
    region: Optional[str] = Query(None, description="Filtrer par région"),
    limit: int = Query(15, description="Nombre maximum de matches"),
    db: Session = Depends(get_db),
):
    """🔥 Algorithme principal : Mise en relation automatique"""
    matches = greedy_matching(db, region=region, top_n=limit)
    return {"status": "success", "matches_count": len(matches), "matches": matches}


@router.post("/route")
def calculate_route(points: List[dict], start_idx: int = 0):
    """Calcul d'itinéraire optimal"""
    if len(points) < 2:
        return {"error": "Minimum 2 points requis"}
    return nearest_neighbor_tsp(points, start_idx)
