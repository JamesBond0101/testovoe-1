from app.enums import Ticker
from app.errors.prices import InvalidPriceDateRangeException, PriceNotFoundException
from app.repositories.prices import PriceRepository
from app.schemas.prices import PriceRecordSchema


class PriceService:
    def __init__(self, repository: PriceRepository) -> None:
        self.repository = repository

    async def get_all(
        self,
        ticker: Ticker,
        page: int,
        page_size: int,
    ) -> list[PriceRecordSchema]:
        records = await self.repository.get_all(ticker, page, page_size)
        return [PriceRecordSchema.model_validate(record) for record in records]

    async def get_latest(self, ticker: Ticker) -> PriceRecordSchema:
        latest_record = await self.repository.get_latest(ticker)
        if latest_record is None:
            raise PriceNotFoundException
        return PriceRecordSchema.model_validate(latest_record)

    async def get_by_date_range(
        self,
        ticker: Ticker,
        date_from: int,
        date_to: int,
    ) -> list[PriceRecordSchema]:
        if date_from > date_to:
            raise InvalidPriceDateRangeException
        records = await self.repository.get_by_date_range(
            ticker,
            date_from,
            date_to,
        )
        return [PriceRecordSchema.model_validate(record) for record in records]
