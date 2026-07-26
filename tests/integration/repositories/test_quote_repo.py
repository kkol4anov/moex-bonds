from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bond import Bond, CouponType, IssuerType
from app.models.quote import Quote
from app.repositories.bond_repo import BondRepository
from app.repositories.quote_repo import QuoteRepository


async def test_add_and_get_quote(session: AsyncSession) -> None:
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

    quote_repo = QuoteRepository(session)
    quote_1 = Quote(
        bond_id=fetched_bond.id,
        quote_date=date(2023, 6, 15),
        clean_price_pct=Decimal("38.39"),
        accrued_interest=Decimal("38.39"),
        volume=Decimal("38.39"),
        bond=fetched_bond,
    )
    await quote_repo.add(quote_1)

    quote_2 = Quote(
        bond_id=fetched_bond.id,
        quote_date=date(2024, 4, 3),
        clean_price_pct=Decimal("38.39"),
        accrued_interest=Decimal("38.39"),
        volume=Decimal("38.39"),
        bond=fetched_bond,
    )
    await quote_repo.add(quote_2)

    fetched_latest = await quote_repo.get_latest(fetched_bond.id)

    assert isinstance(fetched_latest, Quote)

    assert fetched_latest == quote_2