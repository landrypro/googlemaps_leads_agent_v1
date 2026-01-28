from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional

class Lead(BaseModel):
    place_id: str = Field(..., alias="placeId")
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    google_maps_url: Optional[str] = Field(default=None, alias="googleMapsUrl")
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ExportRequest(BaseModel):
    query: str
    centerLat: float
    centerLng: float
    radiusMeters: int = 50000
    limit: int = 500
    enrich: bool = False
