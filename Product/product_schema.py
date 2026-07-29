from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    unit: str
    cost_per_unit: float = Field(gt=0)
    price_per_unit: float = Field(gt=0)
    quantity_in_stock: int = Field(ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(BaseModel):
    id: int
    name: str
    unit: str
    cost_per_unit: float
    price_per_unit: float
    quantity_in_stock: int

    class ConfigDict:
        from_attributes = True