# Butter-Fly-Effect

## Description

Butter-Fly-Effect is a FastAPI web service developed as part of our training. The project simulates a garden center inventory system where users can create, view, and search products. Day 2 introduces Pydantic models, request validation, in-memory storage, and query parameters.

---

## Prerequisites

- Python 3.x
- Git

---

## Clone the Repository

```bash
git clone <repo>
```

---

## Create a Virtual Environment

```bash
python -m venv .venv
```

---

## Activate the Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---



## Run the Application

```bash
uvicorn garden_center.main:app --reload
```

---



## Open the Application

- Home: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---



# Features



## Day 1

- Created a FastAPI application
- Added a root endpoint (`GET /`)
- Added a path parameter endpoint (`GET /hello/{name}`)
- Tested endpoints using Postman
- Ran the application using Uvicorn



## Day 2

- Created a Product model using Pydantic
- Added request body validation
- Stored products in memory
- Created a POST endpoint to add products
- Created a GET endpoint to retrieve all products
- Added a search endpoint using query parameters
- Added validation to prevent negative values

---



## Product Model


| Field             | Type   | Validation                 |
| ----------------- | ------ | -------------------------- |
| name              | string | Required                   |
| unit              | string | Required                   |
| cost_per_unit     | float  | Greater than 0             |
| price_per_unit    | float  | Greater than 0             |
| quantity_in_stock | float  | Greater than or equal to 0 |


---



## API Endpoints


| Method | Endpoint           | Description                             |
| ------ | ------------------ | --------------------------------------- |
| GET    | `/`                | Returns a welcome message               |
| GET    | `/hello/{name}`    | Returns a personalized greeting         |
| POST   | `/products`        | Creates a new product                   |
| GET    | `/products`        | Returns all products                    |
| GET    | `/products/search` | Searches for a product by name and unit |


---



## Example Request

```json
{
  "name": "Basil Plant",
  "unit": "each",
  "cost_per_unit": 1.75,
  "price_per_unit": 4.99,
  "quantity_in_stock": 40
}
```

---



## Validation

The API validates incoming data using Pydantic.

- `cost_per_unit` must be greater than 0.
- `price_per_unit` must be greater than 0.
- `quantity_in_stock` must be greater than or equal to 0.

Invalid requests return a **422 Unprocessable Entity** error.

---



## In-Memory Storage

Products are stored in a Python list while the application is running.

Since no database is connected yet, all data is lost when the server is stopped or restarted.

---



## Tools Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Postman

