from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import Ticker
from app.models.prices import PriceRecord


class PriceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, ticker: Ticker, price: Decimal, timestamp: int) -> None:
        price_record = PriceRecord(
            ticker=ticker,
            price=price,
            timestamp=timestamp,
        )
        self.session.add(price_record)
        await self.session.flush()

    async def get_all(
        self,
        ticker: Ticker,
        page: int,
        page_size: int,
    ) -> list[PriceRecord]:
        stmt = (
            select(PriceRecord)
            .where(PriceRecord.ticker == ticker)
            .order_by(PriceRecord.timestamp.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_latest(self, ticker: Ticker) -> PriceRecord | None:
        stmt = (
            select(PriceRecord)
            .where(PriceRecord.ticker == ticker)
            .order_by(PriceRecord.timestamp.desc())
            .limit(1)
        )
        return await self.session.scalar(stmt)

    async def get_by_date_range(
        self,
        ticker: Ticker,
        date_from: int,
        date_to: int,
    ) -> list[PriceRecord]:
        stmt = (
            select(PriceRecord)
            .where(
                PriceRecord.ticker == ticker,
                PriceRecord.timestamp >= date_from,
                PriceRecord.timestamp <= date_to,
            )
            .order_by(PriceRecord.timestamp.desc())
        )
        result = await self.session.scalars(stmt)
        return list(result.all())
