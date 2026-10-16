from fastapi import FastAPI

from app.api import app_router
from app.core.exception_handlers import register_exception_handlers
from app.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(app_router)
register_exception_handlers(app)


@app.get("/health")
async def health() -> dict:
    return {"message": "OK"}
