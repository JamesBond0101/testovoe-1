from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.repositories.prices import PriceRepository
from app.services.prices import PriceService

SettingsDep = Annotated[Settings, Depends(get_settings)]


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session_factory = request.app.state.session_factory
    async with session_factory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_price_service(session: SessionDep) -> PriceService:
    return PriceService(PriceRepository(session))


PriceServiceDep = Annotated[PriceService, Depends(get_price_service)]