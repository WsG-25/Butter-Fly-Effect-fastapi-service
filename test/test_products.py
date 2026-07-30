from starlette.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_product():
    """
    Test creating a new product.

    Sends a POST request to create a product and verifies:
    - The request is successful (201 Created).
    - The returned product has the expected name.
    """
    response = client.post(
        "/products",
        json={
            "name": "Rose Plant",
            "unit": "each",
            "cost_per_unit": 3.99,
            "price_per_unit": 5.99,
            "quantity_in_stock": 23,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Rose Plant"


def test_create_product_validation():
    """
    Test product validation.

    Sends a POST request with an invalid negative cost_per_unit.
    Verifies that the API returns a 422 validation error.
    """
    response = client.post(
        "/products",
        json={
            "name": "Rose Plant",
            "unit": "each",
            "cost_per_unit": -3.99,
            "price_per_unit": 5.99,
            "quantity_in_stock": 23,
        },
    )

    assert response.status_code == 422


def test_get_product_not_found():
    """
    Test retrieving a product that does not exist.

    Verifies that the API returns:
    - 404 Not Found
    - The correct error message.
    """
    response = client.get("/products/19")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_get_product():
    """
    Test retrieving a product by its ID.

    Verifies that:
    - The request is successful.
    - The response contains a product object.
    - The product fields match the expected values.
    """
    response = client.get("/products/1")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    product = response.json()

    assert product["id"] == 1
    assert product["name"] == "Rose Plant"
    assert product["unit"] == "each"


def test_get_products():
    """
    Test retrieving all products.

    Verifies that:
    - The request is successful.
    - The response is a list.
    - The expected number of products is returned.
    """
    response = client.get("/products")

    assert response.status_code == 200

    products = response.json()

    assert isinstance(products, list)
    assert len(products) == 1


def test_update_product():
    """
    Test updating an existing product.

    First creates a product, then updates it using its ID.
    Verifies that:
    - The update request succeeds.
    - The updated values are returned in the response.
    """
    create_response = client.post(
        "/products",
        json={
            "name": "Test Rose Plant",
            "unit": "each",
            "cost_per_unit": 3.99,
            "price_per_unit": 5.99,
            "quantity_in_stock": 10,
        },
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
            "quantity_in_stock": 999,
        },
    )

    assert response.status_code == 200

    product = response.json()

    assert product["id"] == product_id
    assert product["name"] == "Blue Lotus"
    assert product["quantity_in_stock"] == 999


def test_delete_product_not_found():
    """
        #
    """
    response = client.delete("/products/99999")
    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == "Product not found"


def test_delete_product():
    """
    # Creating test product
    """
    create_response = client.post(
        "/products",
        json={
            "name": "Delete Test Plant",
            "unit": "each",
            "cost_per_unit": 2.99,
            "price_per_unit": 5.99,
            "quantity_in_stock": 10
        }
    )
    assert create_response.status_code == 201

    product_id = create_response.json()["id"]
    
    """
    # Delete the product
    """
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404

