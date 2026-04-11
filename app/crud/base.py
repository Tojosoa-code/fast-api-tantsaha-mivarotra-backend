from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, List, Optional, Any

ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    # === READ ===
    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    # === CREATE ===
    def create(self, db: Session, obj_in: dict):
        obj = self.model(**obj_in)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    # === UPDATE ===
    def update(self, db: Session, id: int, obj_in: dict):
        db_obj = self.get(db, id)
        if db_obj is None:
            return None
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # === DELETE ===
    def delete(self, db: Session, id: int):
        db_obj = self.get(db, id)
        if db_obj is None:
            return None
        db.delete(db_obj)
        db.commit()
        return db_obj
