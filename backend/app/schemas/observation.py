"""Observation and time series schemas for Earthworm."""

from typing import List, Optional
from pydantic import BaseModel, Field


class ObservationPoint(BaseModel):
    date: str
    ndvi: float
    cloud_cover: float = 0.0


class Observation(BaseModel):
    id: str
    farm_id: str
    observed_at: str
    retrieved_at: str
    source: str
    observation_type: str
    metric: str
    value: float
    benchmark_value: float
    unit: str
    quality_flags: str
    status: str
    method: str
    history: List[ObservationPoint] = Field(default_factory=list)
