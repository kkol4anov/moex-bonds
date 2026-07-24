from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Index, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.bond import Bond

class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    bond_id: Mapped[int] = mapped_column(ForeignKey("bonds.id", ondelete="CASCADE"))
    quote_date: Mapped[date] = mapped_column(Date)
    clean_price_pct: Mapped[Decimal] = mapped_column(Numeric(18, 4))
    accrued_interest: Mapped[Decimal] = mapped_column(Numeric(18, 4))
    volume: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))

    bond: Mapped["Bond"] = relationship(back_populates="quotes")

    __table_args__ = (
        Index("ix_quotes_bond_id_quote_date", "bond_id", "quote_date", unique=True),
    )