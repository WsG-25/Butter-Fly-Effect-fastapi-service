from fastapi import FastAPI
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models.product import Product


app = FastAPI()

# DAY 3 - CREATE/DROP DATABASE TABLES

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# DAY 1 ENDPOINTS

@app.get("/")
def root():
    return {"message": "Hello World"}


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