
from starlette.testclient import TestClient as TestClient
from main import app


client = TestClient(app)

def test_create_product():

    response = client.post (
        "/products",
        json={
            "name": "Rose Plant",
            "unit": "each",
            "cost_per_unit": 3.99,
            "price_per_unit": 5.99,
            "quantity_in_stock": 23
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Rose Plant"

def test_create_product_validation():
    response = client.post (
        "/products",
        json={
            "name": "Rose Plant",
            "unit": "each",
            "cost_per_unit": - 3.99,
            "price_per_unit": 5.99,
            "quantity_in_stock": 23
        }
    )

    assert response.status_code == 422