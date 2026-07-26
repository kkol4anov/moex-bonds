from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.favorite import Favorite


class FavoriteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, favorite: Favorite) -> Favorite:
        self._session.add(favorite)
        await self._session.flush()
        return favorite

    async def delete_by_bond(self, bond_id: int) -> None:
        stmt = delete(Favorite).where(Favorite.bond_id == bond_id)
        await self._session.execute(stmt)

    async def list_all(self) -> list[Favorite]:
        stmt = select(Favorite)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())