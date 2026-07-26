from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",    
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    """The common base class. All models are inherired from it.
    Alembic takes Base.metadata for seeing all tables for autogenerate.
    naming_convention makes names and constraints to be predictable.
    """
    
    metadata = MetaData(naming_convention=NAMING_CONVENTION)