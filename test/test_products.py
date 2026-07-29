
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

class TestpProduct:

    def test_get_product(self):
        # Tests get_product function
        response = client.get("/products/1")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)   

        product = response.json()

        assert product["id"] == 1
        assert product["name"] == "Rose Plant"
        assert product["unit"] == "each"  

    def test_get_products(self):

        response = client.get("/products")
        assert response.status_code == 200

        products = response.json()

        assert isinstance(products, list)

        assert len(products) == 1
        

    def test_update_product(self):

        create_response = client.post(
            "/products",
            json={
                "name": "Test Rose Plant",
                "unit": "each",
                "cost_per_unit": 3.99,
                "price_per_unit": 5.99,
                "quantity_in_stock": 10
            }
        )

        assert create_response.status_code == 201

        product_id = create_response.json()["id"]

        response = client.put(
            f"/products/{product_id}",
            json={
                "name": "Blue Lotus",
                "unit": "pouch",
                "cost_per_unit": 5.99,
                "price_per_unit": 7.99,
                "quantity_in_stock": 999
            }
        )

        assert response.status_code == 200

        product = response.json()

        assert product["id"] == product_id
        assert product["name"] == "Blue Lotus"
        assert product["quantity_in_stock"] == 999
