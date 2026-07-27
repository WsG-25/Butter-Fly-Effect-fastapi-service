from fastapi import FastAPI, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import Base, SessionLocal, engine, get_db
from app.models.product import Product
from app.schemas.product import ProductCreate

app = FastAPI()

# DAY 3 - CREATE/DROP DATABASE TABLES

Base.metadata.create_all(bind=engine)


# DAY 1 ENDPOINTS

@app.get("/")
def root():
    return {"message": "Welcome to the Butterfly Garden"}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}



# DAY 3 - DATABASE CONNECTIVITY CHECK

@app.get("/db-check")
def db_check():
    db: Session = SessionLocal()

    try:
        product_count = db.query(func.count(Product.id)).scalar()

        return {
            "database": "Connected",
            "product_count": product_count
        }

    finally:
        db.close()

@app.post("/product")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):

    new_product = Product(
        id=product.id,
        name=product.name,
        price=product.price,
        cost=product.cost,
        quantity=product.quantity
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@app.get("/product/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):

        product = (
    db.query(Product)
      .filter(Product.id == product_id)
      .first()
    )
        
        if product is None:
         return {"Message": "Product not found"}

        return product