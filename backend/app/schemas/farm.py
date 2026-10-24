"""Farm domain schemas for Earthworm."""

from typing import Optional
from pydantic import BaseModel, Field


class FarmBase(BaseModel):
    id: str
    name: str
    district: str
    state: str
    crop: str
    crop_variety: Optional[str] = None
    crop_season: Optional[str] = None
    growth_stage: Optional[str] = None
    survey_plot: Optional[str] = None
    area_hectares: Optional[float] = None
    data_status: str = Field(default="demo", description="Data provenance status: demo, observed, derived")
    satellite_image_url: Optional[str] = None



class Farm(FarmBase):
    pass


class CustomMarkerPoint(BaseModel):
    lat: float
    lng: float


class CustomLandMarker(BaseModel):
    id: str
    farm_id: str = "mandya"
    name: str = "My Custom Field"
    crop: Optional[str] = "Paddy"
    points: list[CustomMarkerPoint] = Field(default_factory=list)
    area_acres: float = Field(default=0.0)
    area_hectares: float = Field(default=0.0)
    centroid: Optional[CustomMarkerPoint] = None
    created_at: str = Field(default="")
    notes: Optional[str] = None
