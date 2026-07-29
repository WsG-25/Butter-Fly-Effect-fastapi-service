from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy import text
from sqlalchemy.orm import Session


from database import (
    engine,
    Base,
    get_db,
    SessionLocal,
)


from Product.product_model import Product as ProductModel


from Product.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)



app = FastAPI(
    title="Butterfly Garden Center API",
    description="Garden center inventory — Butter-Fly-Effect project",
)

STATIC_DIR = Path(__file__).resolve().parent / "static"


def compact_product_ids(db: Session) -> None:
    """Renumber products to 1..n so IDs stay sequential after deletes (demo/dev)."""
    products = (
        db.query(ProductModel)
        .order_by(ProductModel.id.asc())
        .all()
    )

    if not products:
        db.execute(text("ALTER SEQUENCE products_id_seq RESTART WITH 1"))
        db.commit()
        return

    temp_offset = 1_000_000
    for product in products:
        product.id = temp_offset + product.id
    db.flush()

    for index, product in enumerate(products, start=1):
        product.id = index

    db.commit()
    db.execute(
        text(
            "SELECT setval("
            "pg_get_serial_sequence('products', 'id'), "
            "(SELECT COALESCE(MAX(id), 0) FROM products), true)"
        )
    )
    db.commit()


# ----------------------------
# Day 3 Database Setup
# ----------------------------

Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

_startup_db = SessionLocal()
try:
    compact_product_ids(_startup_db)
finally:
    _startup_db.close()



# ----------------------------
# Day 1 Endpoints
# ----------------------------


@app.get("/")
def root():
    return {"message": "Welcome to the Butterfly Garden"}


@app.get("/hello/{name}")
def hello(name:str):

    return {
        "message": f"Hello {name}"
    }



# ----------------------------
# Day 2 In Memory Example
# ----------------------------


day2_products=[]



@app.post(
    "/day2/products",
    status_code=201
)
def create_day2_product(product:ProductCreate):

    day2_products.append(product)

    return product



@app.get("/day2/products")
def get_day2_products():

    return day2_products



# ----------------------------
# Day 3 Database Check
# ----------------------------


@app.get("/db-check")
def db_check(
    db:Session = Depends(get_db)
):

    count = db.query(ProductModel).count()


    return {
        "products_in_database": count
    }


# ==================================================
# Day 4 REAL CRUD USING POSTGRES
# ==================================================



# CREATE PRODUCT
@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    existing_product = (
    db.query(ProductModel)
    .filter(ProductModel.name == product.name)
    .first()
)

    if existing_product:
        raise HTTPException(
            status_code=409,
            detail="A product with that name already exists."
        )

    new_product = ProductModel(

        name = product.name,

        unit = product.unit,

        cost_per_unit = product.cost_per_unit,

        price_per_unit = product.price_per_unit,

        quantity_in_stock = product.quantity_in_stock
    )

    
    db.add(new_product)

    db.commit()

    db.refresh(new_product)


    return new_product





# READ ALL PRODUCTS
@app.get(
    "/products",
    response_model=list[ProductResponse]
)
def get_products(
    db:Session = Depends(get_db)
):


    products = (
        db.query(ProductModel)
        .order_by(ProductModel.id.asc())
        .all()
    )

    return products






# READ SINGLE PRODUCT
@app.get(
    "/products/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id:int,
    db:Session = Depends(get_db)
):


    product = (
        db.query(ProductModel)
        .filter(ProductModel.id == product_id)
        .first()
    )


    if product is None:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    return product





# UPDATE PRODUCT
@app.put(
    "/products/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id:int,
    product_update:ProductUpdate,
    db:Session = Depends(get_db)
):


    product = (
    db.query(ProductModel)
    .filter(ProductModel.id == product_id)
    .first()
)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing_product = (
        db.query(ProductModel)
        .filter(
            ProductModel.name == product_update.name,
            ProductModel.id != product_id
        )
        .first()
    )

    if existing_product:
        raise HTTPException(
            status_code=409,
            detail="A product with that name already exists."
        )


    product.name = product_update.name

    product.unit = product_update.unit

    product.cost_per_unit = product_update.cost_per_unit

    product.price_per_unit = product_update.price_per_unit

    product.quantity_in_stock = product_update.quantity_in_stock



    db.commit()

    db.refresh(product)


    return product





# DELETE PRODUCT
@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id:int,
    db:Session = Depends(get_db)
):


    product = (
        db.query(ProductModel)
        .filter(ProductModel.id == product_id)
        .first()
    )


    if product is None:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )



    db.delete(product)

    db.commit()

    compact_product_ids(db)

    return


# ----------------------------
# Website demo (static UI)
# ----------------------------


@app.get("/demo")
def demo_page():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
