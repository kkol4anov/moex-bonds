from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Index, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.bond import Bond

class Coupon(Base):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(primary_key=True)
    bond_id: Mapped[int] = mapped_column(
        ForeignKey("bonds.id", ondelete="CASCADE"))
    coupon_date: Mapped[date] = mapped_column(Date)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 4))

    bond: Mapped["Bond"] = relationship(back_populates="coupons")

    __table_args__ = (
        Index("ix_coupons_bond_id_coupon_date", "bond_id", "coupon_date"),
    )