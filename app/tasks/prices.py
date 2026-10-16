import asyncio
import logging
from time import time

from app.celery_app import celery_app
from app.clients.deribit_client import DeribitClient
from app.core.config import get_settings
from app.db.session import create_engine, create_session_factory
from app.enums import Ticker
from app.repositories.prices import PriceRepository


logger = logging.getLogger(__name__)
TICKERS = (Ticker.BTC_USD, Ticker.ETH_USD)


async def collect_prices() -> None:
    settings = get_settings()
    engine = create_engine(settings.database_url)
    session_factory = create_session_factory(engine)

    try:
        async with session_factory() as session:
            repository = PriceRepository(session)
            timestamp = int(time())

            async with DeribitClient(str(settings.deribit_base_url)) as client:
                results = await asyncio.gather(
                    *[client.get_price(ticker) for ticker in TICKERS],
                    return_exceptions=True,
                )

            for ticker, result in zip(TICKERS, results):
                if isinstance(result, Exception):
                    logger.exception(
                        "Failed to fetch price for %s",
                        ticker.value,
                        exc_info=result,
                    )
                    continue

                await repository.create(
                    ticker=ticker,
                    price=result,
                    timestamp=timestamp,
                )
            await session.commit()
    except Exception:
        logger.exception("Price collection failed")
        raise
    finally:
        await engine.dispose()


@celery_app.task(name="prices.collect")
def prices_collect() -> None:
    asyncio.run(collect_prices())
