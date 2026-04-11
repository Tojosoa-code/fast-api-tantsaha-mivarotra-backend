from typing import List, Dict
from app.utils.geo import haversine

def nearest_neighbor_tsp(points: List[Dict], start_idx: int = 0) -> Dict:
    """Retourne l'ordre optimal de visite + distance totale"""
    n = len(points)
    if n == 0:
        return {"path": [], "total_distance_km": 0.0}

    visited = [False] * n
    path = [start_idx]
    visited[start_idx] = True
    current = start_idx
    total_distance = 0.0

    for _ in range(n - 1):
        nearest = -1
        min_dist = float('inf')
        for i in range(n):
            if not visited[i]:
                dist = haversine(
                    points[current]["latitude"], points[current]["longitude"],
                    points[i]["latitude"], points[i]["longitude"]
                )
                if dist < min_dist:
                    min_dist = dist
                    nearest = i
        path.append(nearest)
        visited[nearest] = True
        total_distance += min_dist
        current = nearest

    # Retour au point de départ (optionnel pour les livraisons)
    total_distance += haversine(
        points[current]["latitude"], points[current]["longitude"],
        points[start_idx]["latitude"], points[start_idx]["longitude"]
    )
    path.append(start_idx)

    return {
        "path": path,                    # ordre des indices
        "total_distance_km": round(total_distance, 2),
        "points": points                 # pour affichage facile
    }
