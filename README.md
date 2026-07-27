# Butter-Fly-Effect

## Description

Butter-Fly-Effect is a FastAPI web service developed as part of our training. The project simulates a garden center inventory system where users can create, view, search, and manage products.

The project was completed in three phases:

- **Day 1:** Built the FastAPI application and created basic API endpoints.
- **Day 2:** Added Pydantic models, request validation, and in-memory product storage.
- **Day 3:** Connected the application to a PostgreSQL database using SQLAlchemy, replacing the in-memory storage with a persistent database.

---

# Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.x
- Git
- PostgreSQL
- pgAdmin (or psql)

---

# Clone the Repository

```bash
git clone <repository-url>
```

---

# Create a Virtual Environment

```bash
python -m venv .venv
```

---

# Activate the Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

The project uses the following main packages:

- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- psycopg2-binary

---

# PostgreSQL Setup

Make sure PostgreSQL is running before starting the application.

Update the connection string inside **database.py**.

Example:

```python
DATABASE_URL = "postgresql://username:password@localhost:5432/database_name"
```

Replace:

- `username` with your PostgreSQL username
- `password` with your PostgreSQL password
- `database_name` with your team's database name

Default PostgreSQL settings:

- Host: localhost
- Port: 5432

---

# Run the Application

```bash
uvicorn garden_center.main:app --reload
```

---

# Open the Application

| URL | Description |
|------|-------------|
| http://127.0.0.1:8000 | Home endpoint |
| http://127.0.0.1:8000/docs | Swagger UI |
| http://127.0.0.1:8000/redoc | ReDoc |

---

# Features

## Day 1

- Created a FastAPI application
- Added the root endpoint (`GET /`)
- Added a path parameter endpoint (`GET /hello/{name}`)
- Tested endpoints using Postman
- Ran the application using Uvicorn

---

## Day 2

- Created a Product model using Pydantic
- Added request body validation
- Implemented temporary in-memory product storage
- Created a POST endpoint to add products
- Created a GET endpoint to retrieve all products
- Added a search endpoint using query parameters
- Added validation to prevent invalid data

---

## Day 3

- Connected FastAPI to PostgreSQL
- Installed SQLAlchemy and psycopg2-binary
- Created a shared database connection module
- Created a SQLAlchemy Product model
- Replaced the in-memory product list with PostgreSQL storage
- Added automatic table creation using SQLAlchemy
- Added a database connectivity endpoint (`GET /db-check`)
- Verified communication with PostgreSQL

---

# Product Schema

| Field | Type | Validation |
|------|------|------------|
| name | String | Required |
| unit | String | Required |
| cost_per_unit | Float | Greater than 0 |
| price_per_unit | Float | Greater than 0 |
| quantity_in_stock | Float | Greater than or equal to 0 |

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Returns a welcome message |
| GET | `/hello/{name}` | Returns a personalized greeting |
| POST | `/products` | Creates a new product |
| GET | `/products` | Returns all products |
| GET | `/products/search` | Searches for a product by name and unit |
| GET | `/db-check` | Verifies the database connection and returns the current product count |

---

# Example Product Request

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

# Validation

The application uses **Pydantic** to validate incoming request data.

Validation rules include:

- `cost_per_unit` must be greater than 0.
- `price_per_unit` must be greater than 0.
- `quantity_in_stock` must be greater than or equal to 0.

If validation fails, the API returns:

```
422 Unprocessable Entity
```

---

# Database Storage

Starting on **Day 3**, products are stored in a PostgreSQL database instead of an in-memory Python list.

Unlike Day 2, data is stored in the database while the application is running. However, because the schema is recreated on every startup during development, any existing data is removed whenever the application restarts.

---

# Database Structure

The project uses three layers to represent Product data.

## PostgreSQL Table

Stores product records permanently inside the database.

## SQLAlchemy Model

The SQLAlchemy Product model:

- Maps the Python Product class to the PostgreSQL table.
- Creates the database table.
- Reads and writes records.
- Updates and deletes records.
- Represents how data is stored in the database.

## Pydantic Schema

The Pydantic Product schema:

- Validates incoming request data.
- Validates outgoing response data.
- Ensures API requests contain the correct data before reaching the database.

The project uses both because SQLAlchemy manages database operations while Pydantic manages API validation.

---

# Database Connection

The application uses a shared **database.py** module containing:

- **Engine**
- **SessionLocal**
- **Base**

This module centralizes the database configuration so every part of the application uses the same PostgreSQL connection.

---

# Development Database Strategy

During development, the application automatically rebuilds the database schema every time it starts.

The following code runs on startup:

```python
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
```

### Why?

This keeps the database schema synchronized with the SQLAlchemy models while the project is still under development.

> **Warning**
>
> Every time the application starts, all existing tables are dropped and recreated.
>
> This permanently deletes all existing data.
>
> This approach is useful during development but **must never be used in production**, where real customer data needs to be preserved.

---

# Database Connectivity Check

The endpoint

```
GET /db-check
```

opens a database session, verifies that PostgreSQL is reachable, counts the number of Product records, and returns the result.

Example response:

```json
{
  "product_count": 0
}
```

Immediately after restarting the application, the count is expected to be **0** because the database tables are recreated.

---

# Project Structure

```text
garden_center/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
└── README.md
```

---

# Tools Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- psycopg2-binary
- Pydantic
- Uvicorn
- Postman
- pgAdmin / psql

---

