from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetResponse

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("/", response_model=list[AssetResponse])
async def list_assets(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Asset))
    return result.scalars().all()


@router.post("/", response_model=AssetResponse, status_code=201)
async def create_asset(
    asset_data: AssetCreate,
    db: AsyncSession = Depends(get_db),
):
    asset = Asset(**asset_data.model_dump())

    db.add(asset)
    await db.commit()
    await db.refresh(asset)

    return asset
