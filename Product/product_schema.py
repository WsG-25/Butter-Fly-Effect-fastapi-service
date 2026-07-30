from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    unit: str
    cost_per_unit: float = Field(gt=0)
    price_per_unit: float = Field(gt=0)
    quantity_in_stock: int = Field(ge=0)

class ProductCreate(ProductBase):
    category_id: int
    
class ProductUpdate(ProductBase):
    category_id: int

class CategoryInfo(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    unit: str
    cost_per_unit: float
    price_per_unit: float
    quantity_in_stock: int

    class ConfigDict:
        from_attributes = True