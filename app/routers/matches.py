from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.algorithms.matching import greedy_matching
from app.algorithms.routing import nearest_neighbor_tsp
from app.algorithms.trie import product_trie
from app.models.product import Product
from app.models.user import User
from app.models.offer import Offer
from app.models.demand import Demand

router = APIRouter()


@router.get("/search")
def search_products(prefix: str, db: Session = Depends(get_db)):
    product_ids = product_trie.search_prefix(prefix)
    if not product_ids:
        return []
    return db.query(Product).filter(Product.id.in_(product_ids)).all()


@router.post("/match")
def find_matches(
    region: Optional[str] = Query(None),
    limit: int = Query(15),
    db: Session = Depends(get_db),
):
    """Matching amélioré : retourne aussi les noms"""
    matches = greedy_matching(db, region=region, top_n=limit)

    # Enrichissement avec les noms
    enriched = []
    for m in matches:
        offer = db.query(Offer).filter(Offer.id == m["offer_id"]).first()
        demand = db.query(Demand).filter(Demand.id == m["demand_id"]).first()
        product = db.query(Product).filter(Product.id == m["product_id"]).first()
        producteur = db.query(User).filter(User.id == offer.producteur_id).first()
        acheteur = db.query(User).filter(User.id == demand.acheteur_id).first()

        enriched.append(
            {
                **m,
                "product_name": product.nom if product else None,
                "producteur_name": (
                    f"{producteur.prenom} {producteur.nom}" if producteur else None
                ),
                "acheteur_name": (
                    f"{acheteur.prenom} {acheteur.nom}" if acheteur else None
                ),
            }
        )

    return {"status": "success", "matches_count": len(enriched), "matches": enriched}


@router.post("/route")
def calculate_route(points: List[dict], start_idx: int = 0):
    if len(points) < 2:
        return {"error": "Minimum 2 points requis"}
    return nearest_neighbor_tsp(points, start_idx)
