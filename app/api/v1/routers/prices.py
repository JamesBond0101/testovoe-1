from typing import Annotated

from fastapi import APIRouter, Query

from app.dependencies import PriceServiceDep
from app.enums import Ticker
from app.schemas.prices import PriceRecordSchema

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("", response_model=list[PriceRecordSchema])
async def get_prices(
    service: PriceServiceDep,
    ticker: Annotated[Ticker, Query(...)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[PriceRecordSchema]:
    return await service.get_all(ticker, page, page_size)


@router.get("/latest", response_model=PriceRecordSchema)
async def get_latest_price(
    service: PriceServiceDep,
    ticker: Annotated[Ticker, Query(...)],
) -> PriceRecordSchema:
    return await service.get_latest(ticker)


@router.get("/by-date", response_model=list[PriceRecordSchema])
async def get_prices_by_date(
    service: PriceServiceDep,
    ticker: Annotated[Ticker, Query(...)],
    date_from: Annotated[int, Query(...)],
    date_to: Annotated[int, Query(...)],
) -> list[PriceRecordSchema]:
    return await service.get_by_date_range(ticker, date_from, date_to)
