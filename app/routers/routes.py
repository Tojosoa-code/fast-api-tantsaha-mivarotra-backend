from fastapi import APIRouter
from . import auth, users, products, offers, demands, matches

router = APIRouter()

# Auth
router.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Routes
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(products.router, prefix="/products", tags=["Products"])
router.include_router(offers.router, prefix="/offers", tags=["Offers"])
router.include_router(demands.router, prefix="/demands", tags=["Demands"])
router.include_router(
    matches.router, prefix="/matches", tags=["Matching & Algorithmes"]
)
