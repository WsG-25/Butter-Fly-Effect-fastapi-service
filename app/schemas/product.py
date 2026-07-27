from pydantic import BaseModel, Field


<<<<<<< HEAD
class ProductBase(BaseModel):
=======
class ProductCreate(BaseModel):
>>>>>>> a205e10bcd6499af068ac824a35739a45d8771d9
    id : int
    name: str
    unit: str
    cost_per_unit: float = Field(gt=0)
    price_per_unit: float = Field(gt=0)
    quantity_in_stock: float = Field(ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id : int

    class Config:
        from_attributes = True