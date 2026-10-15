from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.enums import Ticker


class BasePriceRecordSchema(BaseModel):
    ticker: Ticker
    price: Decimal
    timestamp: int

    model_config = ConfigDict(from_attributes=True)


class CreatePriceRecordSchema(BasePriceRecordSchema):
    pass


class PriceRecordSchema(BasePriceRecordSchema):
    id: int