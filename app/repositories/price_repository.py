from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import Ticker
from app.models.price import PriceRecord
from app.schemas.price_schemas import PriceRecordSchema


class PriceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, ticker: Ticker, price: Decimal, timestamp: int) -> PriceRecordSchema:
        price_record = PriceRecord(
            ticker=ticker,
            price=price,
            timestamp=timestamp
        )
        self.session.add(price_record)
        await self.session.flush()
        return PriceRecordSchema.model_validate(price_record)