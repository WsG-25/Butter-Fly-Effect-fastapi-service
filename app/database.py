from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
      pass

DATABASE_URL = ("postgresql://postgres:root@localhost:5432/Butterfly-effect")

engine = create_engine("postgresql://postgres:root@localhost:5432/Butterfly-effect")

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

# Base class every SQLAlchemy model inherits from
Base = DeclarativeBase()