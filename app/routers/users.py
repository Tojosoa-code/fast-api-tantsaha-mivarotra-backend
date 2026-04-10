from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.crud.base import CRUDBase

router = APIRouter()
crud_user = CRUDBase(User)

@router.post("/", response_model=UserRead)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Ici on hash le mot de passe plus tard (avec passlib)
    user_dict = user_in.model_dump(exclude={"password"})
    user_dict["password_hash"] = user_in.password  # temporaire
    return crud_user.create(db, user_dict)

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user
