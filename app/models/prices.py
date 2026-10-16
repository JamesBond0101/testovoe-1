from decimal import Decimal

from sqlalchemy import BigInteger, Enum as SqlEnum, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.enums import Ticker


class PriceRecord(Base):
    __tablename__ = "price_records"
    __table_args__ = (
        UniqueConstraint(
            "ticker",
            "timestamp",
            name="uq_price_records_ticker_timestamp",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ticker: Mapped[Ticker] = mapped_column(
        SqlEnum(
            Ticker,
            name="ticker_enum",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
            values_callable=lambda enum_class: [
                ticker.value for ticker in enum_class
            ],
        ),
        nullable=False,
    )
    price: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    timestamp: Mapped[int] = mapped_column(BigInteger, nullable=False)
