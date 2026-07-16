from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """The common base class. All models are inherired from it.
    Alembic takes Base.metadata for seeing all tables for autogenerate."""
    pass