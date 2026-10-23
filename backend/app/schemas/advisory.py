"""Advisory domain schemas for Earthworm."""

from typing import List, Optional
from pydantic import BaseModel, Field


class Advisory(BaseModel):
    id: str
    farm_id: str
    created_at: str
    language: str
    severity: str
    headline: str
    description: str
    metric_summary: str
    notice: str
    meaning: str
    next_steps: List[str]
    sms_preview: str
    voice_transcript: str
    uncertainty_note: str
    data_status: str
