from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fx_rate import FxRate


class FxRateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, fx_rate: FxRate) -> FxRate:
        self._session.add(fx_rate)
        await self._session.flush()
        return fx_rate

    async def get_for(self, currency: str, on_date: date) -> FxRate | None:
        stmt = select(FxRate).where(
            FxRate.currency == currency, FxRate.on_date == on_date
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert(self, values: list[dict[str, Any]]) -> int:
            if not values:
                return 0
            stmt = pg_insert(FxRate).values(values)
            stmt = stmt.on_conflict_do_update(
                index_elements=[FxRate.currency, FxRate.on_date],
                set_={
                    "rate": stmt.excluded.rate,
                },
            )
            result = await self._session.execute(stmt)
            affected_ids = result.scalars().all()
            
            return len(affected_ids)    