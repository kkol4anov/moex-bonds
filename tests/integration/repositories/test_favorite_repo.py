from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bond import Bond, CouponType, IssuerType
from app.models.favorite import Favorite
from app.repositories.bond_repo import BondRepository
from app.repositories.favorite_repo import FavoriteRepository


async def test_add_and_get_favorite_repo(session: AsyncSession) -> None:
    bond_repo = BondRepository(session)
    bond_1 = Bond(
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
    bond_2 = Bond(
        secid="SU26248RMFS3",
        isin="RU000A108EH4",
        short_name="ОФЗ 26248",
        issuer="Минфин России",
        issuer_type=IssuerType.GOVERNMENT,
        coupon_type=CouponType.FIXED,
        currency="RUB",
        face_value=Decimal("1000.0000"),
        issue_date=date(2024, 5, 15),
        maturity_date=date(2040, 5, 16),
        coupon_frequency=2,
    )
    await bond_repo.add(bond_1)
    await bond_repo.add(bond_2)

    fetched_bond_1 = await bond_repo.get_by_secid("SU26230RMFS1")
    fetched_bond_2 = await bond_repo.get_by_secid("SU26248RMFS3")

    assert fetched_bond_1 is not None
    assert fetched_bond_2 is not None

    favourite_repo = FavoriteRepository(session)
    favourite_1 = Favorite(
        bond_id=fetched_bond_1.id,
    )
    favourite_2 = Favorite(
        bond_id=fetched_bond_2.id,
    )
    await favourite_repo.add(favourite_1)
    await favourite_repo.add(favourite_1)
    await favourite_repo.add(favourite_2)

    list_1 = await favourite_repo.list_all()

    await favourite_repo.delete_by_bond(bond_id=fetched_bond_1.id)

    list_2 = await favourite_repo.list_all()

    assert list_1 != []
    assert len(list_1) == 2
    assert (set((favourite_1, favourite_2))) - set(list_1) == set()
    assert (set((favourite_1, favourite_2))) - set(list_2) != set()
    assert (set((favourite_2,))) - set(list_2) == set()