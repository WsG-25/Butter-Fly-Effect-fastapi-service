from fastapi import FastAPI, Depends, HTTPException, status

from sqlalchemy.orm import Session


from app.database import (
    engine,
    Base,
    get_db
)


from app.models.product import Product as ProductModel


from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)



app = FastAPI()



# ----------------------------
# Day 3 Database Setup
# ----------------------------

Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)



# ----------------------------
# Day 1 Endpoints
# ----------------------------


@app.get("/")
def root():

    return {
        "message": "Garden Center API Running"
    }



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


    products = db.query(ProductModel).all()


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


    return