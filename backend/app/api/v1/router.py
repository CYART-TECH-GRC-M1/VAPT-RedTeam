from fastapi import APIRouter

from app.api.v1.assets import router as assets_router


api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(assets_router)