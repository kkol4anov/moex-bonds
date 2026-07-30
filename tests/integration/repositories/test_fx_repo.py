from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fx_rate import FxRate
from app.repositories.fx_rate_repo import FxRateRepository


async def test_add_and_get_fx_rate(session: AsyncSession) -> None:
    repo = FxRateRepository(session)
    fx_rate_1 = FxRate(
        currency="USD",
        on_date=date(2018, 7, 11),
        rate=Decimal("100.0000"),
    )
    fx_rate_2 = FxRate(
        currency="CNY",
        on_date=date(2022, 8, 14),
        rate=Decimal("12.0000"),
    )
    await repo.add(fx_rate_1)
    await repo.add(fx_rate_2)

    fetched_1 = await repo.get_for(currency="USD", on_date=date(2018, 7, 11))
    fetched_2 = await repo.get_for(currency="USD", on_date=date(2022, 8, 14))
    fetched_3 = await repo.get_for(currency="CNY", on_date=date(2022, 8, 14))
    fetched_4 = await repo.get_for(currency="CNY", on_date=date(2018, 7, 11))
    fetched_5 = await repo.get_for(currency="USD", on_date=date(2017, 7, 11))
    fetched_6 = await repo.get_for(currency="CNY", on_date=date(2016, 7, 11))

    assert fetched_1 == fx_rate_1
    assert fetched_2 is None
    assert fetched_3 == fx_rate_2
    assert fetched_4 is None
    assert fetched_5 is None
    assert fetched_6 is None

async def test_upsert_and_get_fx_rate(session: AsyncSession) -> None:
    repo = FxRateRepository(session)
    fx_rate_1 = FxRate(
        currency="USD",
        on_date=date(2018, 7, 11),
        rate=Decimal("100.0000"),
    )
    fx_rate_2 = FxRate(
        currency="CNY",
        on_date=date(2022, 8, 14),
        rate=Decimal("12.0000"),
    )
    await repo.add(fx_rate_1)
    await repo.add(fx_rate_2)

    upsert_values = [
        dict(
            currency="USD",
            on_date=date(2018, 7, 11),
            rate=Decimal("85.0000"),
        )
    ]

    await repo.upsert(upsert_values)
    session.expire_all()

    fetched = await repo.get_for(currency="USD", on_date=date(2018, 7, 11))
    assert fetched is not None

    assert fetched.rate == Decimal("85.0000")