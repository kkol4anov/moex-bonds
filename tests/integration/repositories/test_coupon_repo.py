from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bond import Bond, CouponType, IssuerType
from app.models.coupon import Coupon
from app.repositories.bond_repo import BondRepository
from app.repositories.coupon_repo import CouponRepository


async def test_add_and_get_coupon(session: AsyncSession) -> None:
    bond_repo = BondRepository(session)
    bond = Bond(
        secid="SU26230RMFS1",
        isin="RU000A0ZYQ73",
        short_name="ОФЗ 26230",
        issuer="Минфин России",
        issuer_type=IssuerType.GOVERNMENT,
        coupon_type=CouponType.FIXED,
        currency="RUB",
        face_value=Decimal("1000.0000"),
        issue_date=date(2018, 7, 11),
        maturity_date=date(2039, 3, 16),
        coupon_frequency=2,
    )
    await bond_repo.add(bond)

    fetched_bond = await bond_repo.get_by_secid("SU26230RMFS1")
    assert fetched_bond is not None

    coupon_repo = CouponRepository(session)
    coupon_1 = Coupon(
        bond_id=fetched_bond.id,
        coupon_date=date(2024, 4, 3),
        amount=Decimal("38.39"),
        bond=fetched_bond,
    )
    await coupon_repo.add(coupon_1)

    coupon_2 = Coupon(
        bond_id=fetched_bond.id,
        coupon_date=date(2019, 10, 9),
        amount=Decimal("26.58"),
        bond=fetched_bond,
    )
    await coupon_repo.add(coupon_2)

    fetched_coupon_list = await coupon_repo.list_by_bond(fetched_bond.id)

    assert isinstance(fetched_coupon_list, list)

    assert fetched_coupon_list[0].coupon_date < fetched_coupon_list[1].coupon_date

    for coupon in fetched_coupon_list:
        assert isinstance(coupon.amount, Decimal)
        assert coupon.bond_id == fetched_bond.id
        assert coupon.bond == fetched_bond