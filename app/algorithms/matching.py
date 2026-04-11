from typing import List, Dict
from app.utils.geo import haversine

def calculate_matching_score(offer: Dict, demand: Dict) -> float:
    """Calcule le score de compatibilité (0-100)"""
    dist_km = haversine(
        offer["latitude"], offer["longitude"],
        demand["latitude"], demand["longitude"]
    )

    # Score distance (plus proche = mieux)
    score_distance = max(0, 100 - (dist_km * 1.5))

    # Score prix
    budget = demand.get("budget_max") or float('inf')
    score_prix = 100 if offer["prix_unitaire"] <= budget else max(20, 100 - ((offer["prix_unitaire"] - budget) / budget * 100))

    # Score quantité
    score_quantite = min(100, (float(offer["quantite"]) / float(demand["quantite"])) * 100)

    # Score final pondéré (exactement comme dans le cahier des charges + amélioré)
    return round(0.35 * score_distance + 0.40 * score_prix + 0.25 * score_quantite, 2)

def greedy_matching(offers: List[Dict], demands: List[Dict], top_n: int = 10) -> List[Dict]:
    """Matching glouton : retourne les meilleures correspondances"""
    results = []

    for offer in offers:
        for demand in demands:
            if offer["product_id"] != demand["product_id"]:
                continue
            if offer["region"] != demand["region"]:  # respecte les régions
                continue

            score = calculate_matching_score(offer, demand)
            if score >= 45:  # seuil minimum de pertinence
                results.append({
                    "offer_id": offer["id"],
                    "demand_id": demand["id"],
                    "score": score,
                    "distance_km": round(haversine(
                        offer["latitude"], offer["longitude"],
                        demand["latitude"], demand["longitude"]
                    ), 2),
                    "product_id": offer["product_id"]
                })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]
