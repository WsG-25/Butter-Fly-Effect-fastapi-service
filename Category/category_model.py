<<<<<<< HEAD
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
=======
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
>>>>>>> fef580e00a2adce92d880b03607caa82eb64b9c6

from database import Base


class Category(Base):

    __tablename__ = "categories"

<<<<<<< HEAD
    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String,
        nullable=False,
        unique=True
    )

    products = relationship(
        "Product",
        back_populates="category"
    )
=======
    id: Mapped[int] = mapped_column( Integer, primary_key=True, autoincrement=True, index=True,)

    name: Mapped[str] = mapped_column( String, nullable=False, unique=True,)

    # One category can have many products
    products: Mapped[list["products"]] = relationship( "Product", back_populates="category",)
>>>>>>> fef580e00a2adce92d880b03607caa82eb64b9c6
