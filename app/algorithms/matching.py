from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.offer import Offer
from app.models.demand import Demand
from app.models.match import Match
from app.utils.geo import haversine

"""
Note de compatibilité (0-100) :
- Distance : 35% (100 si <5km, décroissant ensuite)
- Prix : 40% (100 si dans le budget, décroissant si au-dessus)
- Quantité : 25% (100 si offre >= demande, sinon proportionnel)
"""


def calculate_matching_score(offer: Dict, demand: Dict) -> float:
    dist_km = haversine(
        offer["latitude"], offer["longitude"], demand["latitude"], demand["longitude"]
    )

    score_distance = max(0, 100 - (dist_km * 1.5))
    budget = demand.get("budget_max") or float("inf")
    score_prix = (
        100
        if offer["prix_unitaire"] <= budget
        else max(20, 100 - ((offer["prix_unitaire"] - budget) / budget * 100))
    )
    score_quantite = min(
        100, (float(offer["quantite"]) / float(demand["quantite"])) * 100
    )

    return round(0.35 * score_distance + 0.40 * score_prix + 0.25 * score_quantite, 2)


def greedy_matching(db: Session, region: str = None, top_n: int = 15) -> List[Dict]:
    """Algorithme amélioré : calcule + sauvegarde en base"""

    query_offers = db.query(Offer).filter(Offer.statut == "active")
    query_demands = db.query(Demand).filter(Demand.statut == "active")

    if region:
        query_offers = query_offers.filter(Offer.region == region)
        query_demands = query_demands.filter(Demand.region == region)

    offers = query_offers.all()
    demands = query_demands.all()

    results = []

    for offer in offers:
        for demand in demands:
            if offer.product_id != demand.product_id:
                continue

            score = calculate_matching_score(offer.__dict__, demand.__dict__)

            if score >= 45:
                # Sauvegarde dans la table matches
                match = Match(
                    offer_id=offer.id,
                    demand_id=demand.id,
                    score=score,
                    distance_km=round(
                        haversine(
                            offer.latitude,
                            offer.longitude,
                            demand.latitude,
                            demand.longitude,
                        ),
                        2,
                    ),
                )
                db.add(match)
                db.commit()
                db.refresh(match)

                results.append(
                    {
                        "match_id": match.id,
                        "offer_id": offer.id,
                        "demand_id": demand.id,
                        "score": score,
                        "distance_km": match.distance_km,
                        "product_id": offer.product_id,
                        # On pourra ajouter les noms plus tard
                    }
                )

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]
