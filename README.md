# Butter-Fly-Effect

## Description

Butter-Fly-Effect is a FastAPI web service developed as part of our FastAPI training. The application simulates a garden center inventory management system where employees can create, retrieve, update, delete, and organize products into categories.

Throughout the project the application evolved from a simple FastAPI application using in-memory storage into a PostgreSQL-backed REST API using SQLAlchemy, automated testing, environment variables, and relational database modeling.

---

# Features

## Day 1
- FastAPI application setup
- Root endpoint
- Path parameter endpoint
- Postman testing
- Uvicorn development server

## Day 2
- Pydantic request validation
- Product request model
- In-memory product storage
- Search endpoint using query parameters

## Day 3
- PostgreSQL integration
- SQLAlchemy Product model
- Shared database connection
- Automatic database creation
- Database connectivity endpoint

## Day 4
- Create Product
- Retrieve all Products
- Retrieve Product by ID
- Dependency injection using `get_db`
- Response models

## Day 5
- Update Products
- Delete Products
- HTTPException error handling
- 404 responses for missing products
- Validation improvements

## Day 6
- Automated testing with Pytest
- FastAPI TestClient
- Environment variables using `.env`
- Removed hardcoded database credentials
- Regression testing

## Day 7
- Added Category model
- One-to-many relationship between Categories and Products
- Foreign key constraints
- Nested API responses
- Category creation endpoint
- Product creation with Category assignment
- Retrieve Categories with all associated Products

---

# Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- psycopg2-binary
- Pytest
- HTTPX
- python-dotenv
- Uvicorn
- Postman
- pgAdmin / psql

---

# Prerequisites

Before running the project install:

- Python 3.x
- PostgreSQL
- Git

---

# Clone the Repository

```bash
git clone <repository-url>
cd Butter-Fly-Effect
```

---

# Create a Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```text
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

Replace:

- username
- password
- database_name

The `.env` file should never be committed to source control.

---

# Run the Application

```bash
uvicorn main:app --reload
```

---

# Run the Test Suite

```bash
pytest
```

The automated tests verify:

- Product creation
- Validation failures
- Not-found responses
- CRUD functionality

---

# API Documentation

Once the application is running:

| URL | Description |
|------|-------------|
| http://127.0.0.1:8000 | Root endpoint |
| http://127.0.0.1:8000/docs | Swagger UI |
| http://127.0.0.1:8000/redoc | ReDoc |

---

# Product Model

| Field | Type |
|---------|------|
| id | Integer |
| name | String |
| unit | String |
| cost_per_unit | Float |
| price_per_unit | Float |
| quantity_in_stock | Float |
| category_id | Integer (Foreign Key) |

---

# Category Model

| Field | Type |
|---------|------|
| id | Integer |
| name | String |

Each Category may contain many Products.

Each Product belongs to one Category.

---

# Validation

The API validates requests using Pydantic.

Examples include:

- Required fields
- Positive prices
- Positive costs
- Non-negative inventory
- Valid data types

If validation fails, FastAPI returns:

```
422 Unprocessable Entity
```

If a requested resource cannot be found:

```
404 Not Found
```

If a Product references a Category that does not exist, the API returns an appropriate client error instead of allowing the database exception to become a server error.

---

# Database

The application stores data in PostgreSQL using SQLAlchemy.

The project contains:

- SQLAlchemy Models
- Pydantic Schemas
- Shared database connection
- SQLAlchemy Sessions

During development the application recreates the schema each time it starts:

```python
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
```

This keeps the database synchronized with the models during development.

> **Warning**
>
> This deletes all existing data each time the application starts.
> It should only be used during development.

---

# API Endpoints

## Products

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /products | Create Product |
| GET | /products | Retrieve all Products |
| GET | /products/{id} | Retrieve Product |
| PUT | /products/{id} | Update Product |
| DELETE | /products/{id} | Delete Product |

## Categories

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /categories | Create Category |
| GET | /categories/{id} | Retrieve Category with Products |

---

# Database Relationship

The project models a **one-to-many relationship**.

```
Category
    │
    ├── Product
    ├── Product
    ├── Product
```

Each Product stores a `category_id` foreign key that references the Category table.

This ensures a Product cannot reference a Category that does not exist.

---

# Testing

Automated tests are written using:

- Pytest
- FastAPI TestClient

The test suite verifies:

- Successful requests
- Validation failures
- Not-found responses
- CRUD operations
- Database integration

---

# Contributors

See `CONTRIBUTORS.md` for the project contributors.