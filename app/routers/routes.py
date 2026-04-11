from fastapi import APIRouter
from . import users, products, offers, demands, matches, auth

router = APIRouter()

router.include_router(auth.router, prefix="/api/v1")
router.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
router.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
router.include_router(offers.router, prefix="/api/v1/offers", tags=["Offers"])
router.include_router(demands.router, prefix="/api/v1/demands", tags=["Demands"])
router.include_router(
    matches.router, prefix="/api/v1/matches", tags=["Matching & Algorithmes"]
)
