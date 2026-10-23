"""Farm, observation, advisory, and weather endpoints."""

from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from app.data.demo.fixtures import (
    DEMO_ADVISORIES,
    DEMO_FARMS,
    DEMO_OBSERVATIONS,
    DEMO_WEATHER,
)
from app.schemas.advisory import Advisory
from app.schemas.communication import CommunicationPreview
from app.schemas.farm import Farm
from app.schemas.observation import Observation

router = APIRouter()


@router.get("/farms", response_model=List[Farm], summary="List All Monitored Farms")
def list_farms() -> List[Farm]:
    """Retrieve all available farms (pan-India demo set)."""
    return [Farm(**farm) for farm in DEMO_FARMS]


@router.get("/farms/{farm_id}", response_model=Farm, summary="Get Farm Details")
def get_farm(farm_id: str) -> Farm:
    """Retrieve details for a specific farm by ID."""
    farm = next((f for f in DEMO_FARMS if f["id"] == farm_id.lower()), None)
    if not farm:
        raise HTTPException(status_code=404, detail=f"Farm '{farm_id}' not found.")
    return Farm(**farm)


@router.get("/farms/{farm_id}/observations", response_model=Observation, summary="Get Latest Satellite Observations")
def get_farm_observations(farm_id: str) -> Observation:
    """Retrieve latest satellite vegetation observation with historical time-series."""
    obs = DEMO_OBSERVATIONS.get(farm_id.lower())
    if not obs:
        raise HTTPException(status_code=404, detail=f"No observations found for farm '{farm_id}'.")
    return Observation(**obs)


@router.get("/farms/{farm_id}/advisory", response_model=Advisory, summary="Get Explainable Farm Advisory")
def get_farm_advisory(
    farm_id: str,
    language: str = Query(default="en", description="Language code: en, kn, hi"),
) -> Advisory:
    """Retrieve 3-stage explainable agronomic advisory in selected language with fallback."""
    farm_id_clean = farm_id.lower()
    lang_clean = language.lower()

    # Look for specific language, falling back to English
    advisory_data = DEMO_ADVISORIES.get((farm_id_clean, lang_clean)) or DEMO_ADVISORIES.get((farm_id_clean, "en"))
    if not advisory_data:
        raise HTTPException(status_code=404, detail=f"No advisory found for farm '{farm_id}'.")

    return Advisory(**advisory_data)


@router.get(
    "/farms/{farm_id}/communications/preview",
    response_model=CommunicationPreview,
    summary="Get SMS/Voice Communication Preview",
)
def get_communication_preview(
    farm_id: str,
    language: str = Query(default="en", description="Language code: en, kn, hi"),
    channel: str = Query(default="sms", description="Channel: sms or voice"),
) -> CommunicationPreview:
    """Preview advisory text formatted for SMS or Voice readout simulation."""
    advisory = get_farm_advisory(farm_id=farm_id, language=language)

    if channel.lower() == "voice":
        preview_text = advisory.voice_transcript
    else:
        preview_text = advisory.sms_preview

    return CommunicationPreview(
        id=f"comm_{farm_id}_{channel}_{language}",
        farm_id=farm_id,
        language=language,
        channel=channel,
        preview_text=preview_text,
        char_count=len(preview_text),
        status="preview_only",
        created_at=datetime.now(timezone.utc).isoformat(),
    )


@router.get("/farms/{farm_id}/weather", summary="Get Regional Weather Outlook")
def get_farm_weather(farm_id: str):
    """Retrieve 3-day weather outlook and recommendations."""
    weather = DEMO_WEATHER.get(farm_id.lower())
    if not weather:
        raise HTTPException(status_code=404, detail=f"No weather data for farm '{farm_id}'.")
    return weather
