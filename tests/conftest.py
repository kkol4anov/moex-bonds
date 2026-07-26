from collections.abc import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.community.postgres import PostgresContainer

from app import models  # noqa: F401  — register all models in Base.metadata
from app.db.base import Base


@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    with PostgresContainer("postgres:16") as container:
        yield container


@pytest.fixture(scope="session")
def async_db_url(postgres_container: PostgresContainer) -> str:
    # testcontainers checks by sync driver (psycopg2),
    # so get_connection_url() returns postgresql+psycopg2://.
    # App needs asyncpg so we change the driver.
    sync_url = postgres_container.get_connection_url()
    return sync_url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)

@pytest_asyncio.fixture(scope="session")
async def engine(async_db_url: str) -> AsyncIterator[AsyncEngine]:
    eng = create_async_engine(async_db_url, pool_pre_ping=True)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    await eng.dispose()


@pytest_asyncio.fixture
async def session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    async with engine.connect() as connection:
        async with connection.begin():
            maker = async_sessionmaker(
                bind=connection,
                expire_on_commit=False,
                join_transaction_mode="create_savepoint",
            )
            db_session = maker()

            try:
                yield db_session
            finally:
                await db_session.close()