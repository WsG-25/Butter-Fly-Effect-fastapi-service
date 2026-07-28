from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True,index=True)

    name: Mapped[str] = mapped_column(String, nullable=False)

    unit: Mapped[str] = mapped_column(String, nullable=False)

    cost_per_unit: Mapped[float] = mapped_column(Float, nullable=False)

    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False)

    quantity_in_stock: Mapped[int] = mapped_column(Integer, nullable=False)