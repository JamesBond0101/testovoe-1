from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession



def create_engine(url: PostgresDsn) -> AsyncEngine:
    return create_async_engine(
        str(url),
        echo=False,
    )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)