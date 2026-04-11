from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base, SessionLocal
from app.routers import routes
from app.routers.matches import product_trie  # ← important
from app.models.product import Product

# Création des tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tantsaha Mivarotra API",
    description="Plateforme de commerce agricole - Backend FastAPI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Charger le Trie au démarrage
def load_trie():
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        for p in products:
            product_trie.insert(p.nom, p.id)
        print(f"✅ Trie chargé avec {len(products)} produits")
    finally:
        db.close()


load_trie()

app.include_router(routes.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "🚀 Tantsaha Mivarotra Backend est en ligne ! Algorithmes activés."
    }
