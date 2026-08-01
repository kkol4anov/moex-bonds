from typing import Any

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.coupon import Coupon


class CouponRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, coupon: Coupon) -> Coupon:
        self._session.add(coupon)
        await self._session.flush()
        return coupon

    async def list_by_bond(self, bond_id: int) -> list[Coupon]:
        stmt = select(Coupon).where(Coupon.bond_id == bond_id).order_by(Coupon.coupon_date)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def replace_for_bond(self, bond_id: int, values: list[dict[str, Any]]) -> int:
        await self._session.execute(delete(Coupon).where(Coupon.bond_id == bond_id))
        if not values:
            return 0
        await self._session.execute(insert(Coupon), values)
        return len(values)