from sqlalchemy import select
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