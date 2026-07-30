from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column( Integer, primary_key=True, autoincrement=True, index=True,)

    name: Mapped[str] = mapped_column( String, nullable=False, unique=True,)

    # One category can have many products
    products: Mapped[list["products"]] = relationship( "Product", back_populates="category",)