from fastapi import FastAPI
from garden_center.models.product import Product

app = FastAPI()

products = []

@app.get("/")
def root():
    return {"message": "Welcome to the Garden Center"}

@app.post("/products", status_code=201)
def create_product(product: Product):
    products.append(product) 
    return product

@app.get("/products")
def get_products():
    return products

@app.get("/products/search")
def product_search(name: str, unit: str = "each"):
    for product in products:
        if (
            product.name.lower() == name.lower()
            and product.unit.lower() == unit.lower()
        ):
            return product

    return {"message": "Product not found"}