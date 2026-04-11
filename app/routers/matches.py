from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.offer import Offer
from app.models.demand import Demand
from app.models.product import Product
from app.algorithms.matching import greedy_matching
from app.algorithms.routing import nearest_neighbor_tsp
from app.algorithms.trie import ProductTrie
import json

router = APIRouter()

# Trie global chargé au démarrage (on le remplit plus bas)
product_trie = ProductTrie()

@router.get("/search")
def search_products(prefix: str, db: Session = Depends(get_db)):
    """Recherche rapide avec auto-complétion (utilise le Trie)"""
    product_ids = product_trie.search_prefix(prefix)
    if not product_ids:
        return []
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    return products

@router.post("/match")
def find_matches(
    region: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Mise en relation automatique (Algorithme principal)"""
    offers = db.query(Offer).filter(Offer.statut == "active").all()
    demands = db.query(Demand).filter(Demand.statut == "active").all()

    # Conversion en dict pour l'algo
    offers_dict = [o.__dict__ for o in offers]
    demands_dict = [d.__dict__ for d in demands]

    if region:
        offers_dict = [o for o in offers_dict if o["region"] == region]
        demands_dict = [d for d in demands_dict if d["region"] == region]

    matches = greedy_matching(offers_dict, demands_dict, top_n=limit)
    return {"matches": matches, "count": len(matches)}

@router.post("/route")
def calculate_route(
    points: List[dict],  # liste de {"latitude": , "longitude": , "name": optional}
    start_idx: int = 0
):
    """Calcul d'itinéraire optimal pour plusieurs points"""
    if len(points) < 2:
        return {"error": "Il faut au moins 2 points"}
    result = nearest_neighbor_tsp(points, start_idx)
    return result
