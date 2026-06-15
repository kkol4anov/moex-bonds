from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Общий базовый класс. От него наследуются все модели.
    Alembic берёт Base.metadata, чтобы видеть все таблицы для autogenerate."""
    pass