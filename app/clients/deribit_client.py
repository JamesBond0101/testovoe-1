from decimal import Decimal
from typing import Any

import aiohttp

from app.enums import Ticker


class DeribitClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "DeribitClient":
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.session is not None:
            await self.session.close()

    async def get_price(self, ticker: Ticker) -> Decimal:
        if self.session is None:
            raise RuntimeError("DeribitClient must be used as an async context manager")

        params = {"index_name": ticker.value}
        async with self.session.get(self.base_url, params=params) as response:
            response.raise_for_status()
            payload = await response.json()

        try:
            index_price = payload["result"]["index_price"]
        except (KeyError, TypeError) as error:
            raise ValueError(
                f"Unexpected Deribit response for {ticker.value}"
            ) from error

        return Decimal(str(index_price))
