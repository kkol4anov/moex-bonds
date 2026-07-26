from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
	from app.models.coupon import Coupon
	from app.models.quote import Quote

class CouponType(StrEnum):
	FLOAT = "FLOAT"
	FIXED = "FIXED"
	ZERO = "ZERO" #DISCOUNT
	VARIABLE = "VARIABLE"
	
	
class IssuerType(StrEnum):
	GOVERNMENT = "GOVERNMENT"
	MUNICIPAL = "MUNICIPAL"
	CORPORATE = "CORPORATE"
	FOREIGN = "FOREIGN"
	

class Bond(Base):
    __tablename__ = "bonds"

    id: Mapped[int] = mapped_column(primary_key=True)
    secid: Mapped[str] = mapped_column(String(36), unique=True)
    isin: Mapped[str | None] = mapped_column(String(12))
    short_name: Mapped[str] = mapped_column(String(255))
    issuer: Mapped[str] = mapped_column(String(255))
    issuer_type: Mapped[IssuerType]
    currency: Mapped[str] = mapped_column(String(3))
    face_value: Mapped[Decimal] = mapped_column(Numeric(18, 4))
    issue_date: Mapped[date] = mapped_column(Date)
    maturity_date: Mapped[date] = mapped_column(Date, index=True)
    coupon_frequency: Mapped[int]
    coupon_type: Mapped[CouponType]
    coupons: Mapped[list["Coupon"]] = relationship(
        back_populates="bond", cascade="all, delete-orphan"
    )
    quotes: Mapped[list["Quote"]] = relationship(
        back_populates="bond", cascade="all, delete-orphan"
    )