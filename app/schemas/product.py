from pydantic import BaseModel, Field


class Product(BaseModel):
    id : int
    name: str
    unit: str
    cost_per_unit: float = Field(gt=0)
    price_per_unit: float = Field(gt=0)
<<<<<<< HEAD
    quantity_in_stock: float = Field(ge=0)
=======
    quantity_in_stock: float = Field(ge=0)
>>>>>>> 993293c4830c988a7063badb5e8b0f1b360f346b
