from fastapi.testclient import TestClient
from main import app, hello, compact_product_ids, root, db_check, create_product, get_products, update_product,delete_product
from Product.product_model import Product
