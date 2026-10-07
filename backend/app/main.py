from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "vapt-redteam-api",
    }