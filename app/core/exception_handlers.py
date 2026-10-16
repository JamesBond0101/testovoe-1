from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors.prices import InvalidPriceDateRangeException, PriceNotFoundException


async def price_not_found_handler(
    _request: Request,
    _exc: PriceNotFoundException,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": "Price not found"},
    )


async def invalid_price_date_range_handler(
    _request: Request,
    _exc: InvalidPriceDateRangeException,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": "date_from must be less than or equal to date_to"},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(PriceNotFoundException, price_not_found_handler)
    app.add_exception_handler(
        InvalidPriceDateRangeException,
        invalid_price_date_range_handler,
    )
