from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bond import Bond


class BondRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, bond: Bond) -> Bond:
        self._session.add(bond)
        await self._session.flush()
        return bond

    async def get_by_secid(self, secid: str) -> Bond | None:
        stmt = select(Bond).where(Bond.secid == secid)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert(self, values: list[dict[str, Any]]) -> int:
        """Inserts or updates bonds by natural key (secid). Returns amount of affected rows."""
        if not values:
            return 0

        insert_stmt = pg_insert(Bond).values(values)
        update_columns = {
            column.name: insert_stmt.excluded[column.name]
            for column in Bond.__table__.columns
            if column.name not in ("id", "secid")
        }
        stmt = insert_stmt.on_conflict_do_update(
            index_elements=[Bond.secid],
            set_=update_columns,
        ).returning(Bond.secid)
        result = await self._session.execute(stmt)

        affected_ids = result.scalars().all()

        return len(affected_ids)