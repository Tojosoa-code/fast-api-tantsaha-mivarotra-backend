from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash, create_access_token, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    user_dict = user_in.model_dump(exclude={"password"})
    user_dict["password_hash"] = get_password_hash(user_in.password)

    user = User(**user_dict)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": user}
