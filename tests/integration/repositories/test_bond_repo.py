from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bond import Bond, CouponType, IssuerType
from app.repositories.bond_repo import BondRepository


async def test_add_and_get_bond(session: AsyncSession) -> None:
    repo = BondRepository(session)
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
    await repo.add(bond)

    fetched = await repo.get_by_secid("SU26230RMFS1")

    assert fetched is not None
    assert fetched.secid == "SU26230RMFS1"
    # Is Decimal and is not float — check value and type (asyncpg ↔ Numeric)
    assert isinstance(fetched.face_value, Decimal)
    assert fetched.face_value == Decimal("1000.0000")
    assert fetched.issuer_type is IssuerType.GOVERNMENT


async def test_get_by_secid_missing_returns_none(session: AsyncSession) -> None:
    repo = BondRepository(session)
    assert await repo.get_by_secid("NOPE") is None

async def test_upsert_and_get_bond(session: AsyncSession) -> None:
    repo = BondRepository(session)
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

    upsert_values = [
        dict(
            secid="SU26230RMFS1",
            isin="RU000A0ZYQ73",
            short_name="UPSERTED_NAME",
            issuer="Минфин России",
            issuer_type=IssuerType.GOVERNMENT,
            coupon_type=CouponType.ZERO,
            currency="RUB",            
            face_value=Decimal("500.0000"),
            issue_date=date(2018, 7, 11),
            maturity_date=date(2039, 3, 16),
            coupon_frequency=2,
        )
    ]

    await repo.add(bond)
    
    affected_rows = await repo.upsert(upsert_values)
    session.expire_all()

    assert affected_rows > 0

    fetched = await repo.get_by_secid("SU26230RMFS1")

    assert fetched is not None
    assert fetched.secid == "SU26230RMFS1"
    assert fetched.short_name == "UPSERTED_NAME"
    assert fetched.coupon_type == CouponType.ZERO
    assert fetched.face_value == Decimal("500.0000")