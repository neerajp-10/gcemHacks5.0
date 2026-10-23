"""Communication preview schemas for SMS and Voice."""

from pydantic import BaseModel, Field


class CommunicationPreview(BaseModel):
    id: str
    farm_id: str
    language: str
    channel: str
    preview_text: str
    audio_url: str = ""
    status: str = Field(default="preview_only", description="preview_only, simulated, delivered")
    char_count: int
    created_at: str
