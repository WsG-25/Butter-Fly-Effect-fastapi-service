from fastapi import FastAPI
from models.model import Product
app = FastAPI()

product = []

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/products/search")
def product_search(name: str, unit: str ="each"):
    return Product

@app.post("/products", status_code=201)
def create_product(product: Product):
    product.append(product)
    return product