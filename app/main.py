from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routers import routes

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

app.include_router(routes.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "🚀 Tantsaha Mivarotra Backend est en ligne !"}
