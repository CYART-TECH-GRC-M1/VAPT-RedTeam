import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AssetCreate(BaseModel):
    tenant_id: uuid.UUID

    name: str = Field(min_length=1, max_length=255)

    asset_type: str = Field(
        min_length=1,
        max_length=50,
    )

    hostname: str | None = None

    ip_address: str | None = None

    criticality: str = "medium"

    description: str | None = None


class AssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    asset_type: str
    hostname: str | None
    ip_address: str | None
    criticality: str
    description: str | None
    created_at: datetime
    updated_at: datetime