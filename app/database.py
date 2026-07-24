from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
      pass

DATABASE_URL = ("postgresql://postgres:root@localhost:5432/Butterfly-effect")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create database sessions
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

# Base class for all models
Base = DeclarativeBase()