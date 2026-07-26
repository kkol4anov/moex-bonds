from sqlalchemy import select
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