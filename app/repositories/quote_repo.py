from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quote import Quote


class QuoteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, quote: Quote) -> Quote:
        self._session.add(quote)
        await self._session.flush()
        return quote

    async def get_latest(self, bond_id: int) -> Quote | None:
            stmt = (
                select(Quote)
                .where(Quote.bond_id == bond_id)
                .order_by(Quote.quote_date.desc())
                .limit(1)
            )
            result = await self._session.execute(stmt)
            return result.scalar_one_or_none()

    async def upsert(self, values: list[dict[str, Any]]) -> int:
            if not values:
                return 0
            stmt = pg_insert(Quote).values(values)
            stmt = stmt.on_conflict_do_update(
                index_elements=[Quote.bond_id, Quote.quote_date],
                set_={
                    "clean_price_pct": stmt.excluded.clean_price_pct,
                    "accrued_interest": stmt.excluded.accrued_interest,
                    "volume": stmt.excluded.volume,
                },
            )
            result = await self._session.execute(stmt)
            affected_ids = result.scalars().all()
            
            return len(affected_ids)