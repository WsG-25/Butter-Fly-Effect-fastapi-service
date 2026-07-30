from pydantic import BaseModel


class ProductInCategory(BaseModel):
    id: int
    name: str
    unit: str
    cost_per_unit: float
    price_per_unit: float
    quantity_in_stock: int

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CategoryWithProducts(BaseModel):
    id: int
    name: str
    products: list[ProductInCategory]

    class Config:
        from_attributes = True