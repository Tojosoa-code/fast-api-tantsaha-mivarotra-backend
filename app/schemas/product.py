from pydantic import BaseModel

class ProductBase(BaseModel):
    nom: str
    categorie: str
    description: str | None = None
    unite: str = "kg"

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True
