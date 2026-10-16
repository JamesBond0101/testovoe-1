from fastapi import APIRouter

from app.api.v1.routers.prices import router as prices_router

app_router = APIRouter(prefix="/api/v1")
app_router.include_router(prices_router)