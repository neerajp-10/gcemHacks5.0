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


class Farm(FarmBase):
    pass
