from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    nom: str
    prenom: str
    telephone: str
    latitude: float
    longitude: float
    region: str = Field(..., description="Région (Analamanga, Atsinanana, etc.)")
    adresse: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: str = Field(..., pattern="^(producteur|acheteur|admin)$")

class UserRead(UserBase):
    id: int
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True
