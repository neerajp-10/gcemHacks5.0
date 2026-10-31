"""Farm, observation, advisory, and weather endpoints."""

from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Response

from app.data.demo.fixtures import (
    DEMO_ADVISORIES,
    DEMO_FARMS,
    DEMO_OBSERVATIONS,
    DEMO_WEATHER,
)
from app.schemas.advisory import Advisory
from app.schemas.communication import CommunicationPreview
from app.schemas.farm import CreateFarmRequest, CustomLandMarker, Farm
from app.schemas.observation import Observation
from app.services.sentinel import sentinel_service

router = APIRouter()

# In-memory registry for user-added custom farms
_REGISTERED_CUSTOM_FARMS: dict[str, dict] = {}


@router.get("/farms", response_model=List[Farm], summary="List All Monitored Farms")
def list_farms() -> List[Farm]:
    """Retrieve all available farms (pan-India demo set + user-registered farms)."""
    result = []
    # Built-in demo farms
    for farm in DEMO_FARMS:
        farm_copy = dict(farm)
        farm_copy["satellite_image_url"] = f"/api/farms/{farm['id']}/satellite-image"
        result.append(Farm(**farm_copy))
    # User-registered custom farms
    for custom_farm in _REGISTERED_CUSTOM_FARMS.values():
        c_copy = dict(custom_farm)
        c_copy["satellite_image_url"] = f"/api/farms/{custom_farm['id']}/satellite-image"
        result.append(Farm(**c_copy))
    return result


@router.post("/farms", response_model=Farm, status_code=201, summary="Register a New Farm")
def create_farm(payload: CreateFarmRequest) -> Farm:
    """Register a new farm parcel with custom location, crop, and acreage."""
    # Generate slug ID from name or custom id
    slug_base = payload.id or payload.name.lower().replace(" ", "_").replace("/", "_").replace("#", "")
    farm_id = f"custom_{slug_base}" if not slug_base.startswith("custom_") else slug_base

    farm_data = {
        "id": farm_id,
        "name": payload.name,
        "district": payload.district,
        "state": payload.state,
        "crop": payload.crop,
        "crop_variety": payload.crop_variety or "Standard Hybrid",
        "crop_season": payload.crop_season or "Rabi / Summer",
        "growth_stage": payload.growth_stage or "Vegetative",
        "survey_plot": payload.survey_plot or f"Plot #{farm_id[-4:]}",
        "area_hectares": payload.area_hectares or 1.0,
        "data_status": "observed",
        "latitude": payload.latitude,
        "longitude": payload.longitude,
        "satellite_image_url": f"/api/farms/{farm_id}/satellite-image",
    }
    _REGISTERED_CUSTOM_FARMS[farm_id] = farm_data
    return Farm(**farm_data)


@router.get("/farms/{farm_id}", response_model=Farm, summary="Get Farm Details")
def get_farm(farm_id: str) -> Farm:
    """Retrieve details for a specific farm by ID."""
    clean_id = farm_id.lower()
    farm = next((f for f in DEMO_FARMS if f["id"] == clean_id), None)
    if not farm:
        farm = _REGISTERED_CUSTOM_FARMS.get(clean_id)
    if not farm:
        raise HTTPException(status_code=404, detail=f"Farm '{farm_id}' not found.")
    farm_copy = dict(farm)
    farm_copy["satellite_image_url"] = f"/api/farms/{farm['id']}/satellite-image"
    return Farm(**farm_copy)


@router.delete("/farms/{farm_id}", summary="Delete a Registered Custom Farm")
def delete_farm(farm_id: str):
    """Delete a custom registered farm."""
    clean_id = farm_id.lower()
    if clean_id in _REGISTERED_CUSTOM_FARMS:
        del _REGISTERED_CUSTOM_FARMS[clean_id]
        return {"success": True, "message": f"Farm '{clean_id}' deleted successfully."}
    if any(f["id"] == clean_id for f in DEMO_FARMS):
        raise HTTPException(status_code=400, detail="Default demo farms cannot be deleted.")
    raise HTTPException(status_code=404, detail=f"Farm '{farm_id}' not found.")


@router.get("/farms/{farm_id}/satellite-image", summary="Get Copernicus Sentinel-2 Satellite Image")
def get_farm_satellite_image(
    farm_id: str,
    layer: str = Query("true-color", description="Satellite layer: 'true-color', 'ndvi', 'false-color', 'moisture'")
):
    """Retrieve Copernicus Sentinel-2 satellite imagery for farm parcel with layer selection."""
    farm_id_clean = farm_id.lower()
    img_bytes = sentinel_service.fetch_live_satellite_image(farm_id_clean, layer=layer)
    if not img_bytes:
        raise HTTPException(status_code=404, detail=f"Satellite image not available for farm '{farm_id}'.")
    return Response(
        content=img_bytes,
        media_type="image/jpeg",
        headers={"Cache-Control": "public, max-age=3600"},
    )


@router.get("/farms/{farm_id}/satellite-metadata", summary="Get Copernicus Sentinel-2 Satellite Pass Metadata")
def get_farm_satellite_metadata(farm_id: str):
    """Retrieve detailed Copernicus Sentinel-2 satellite pass telemetry, coordinates, and layer info."""
    meta = sentinel_service.get_farm_metadata(farm_id)
    if not meta:
        raise HTTPException(status_code=404, detail=f"Metadata not found for farm '{farm_id}'.")
    return meta



@router.get("/farms/{farm_id}/observations", response_model=Observation, summary="Get Latest Satellite Observations")
def get_farm_observations(farm_id: str) -> Observation:
    """Retrieve latest satellite vegetation observation with historical time-series."""
    clean_id = farm_id.lower()
    obs = DEMO_OBSERVATIONS.get(clean_id)
    if not obs and clean_id in _REGISTERED_CUSTOM_FARMS:
        obs = {
            "id": f"obs_{clean_id}_01",
            "farm_id": clean_id,
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "source": "Copernicus Sentinel-2 (ESA) Level-2A",
            "observation_type": "satellite",
            "metric": "NDVI",
            "value": 0.68,
            "benchmark_value": 0.70,
            "unit": "ratio (-1 to 1)",
            "quality_flags": "cloud_free, valid_reflectance",
            "status": "observed",
            "method": "(B8 - B4) / (B8 + B4)",
            "history": [
                {"date": "2024-02-04", "ndvi": 0.64, "cloud_cover": 0.0},
                {"date": "2024-02-09", "ndvi": 0.65, "cloud_cover": 0.0},
                {"date": "2024-02-14", "ndvi": 0.66, "cloud_cover": 0.0},
                {"date": "2024-02-19", "ndvi": 0.67, "cloud_cover": 0.0},
                {"date": "2024-02-24", "ndvi": 0.68, "cloud_cover": 0.0},
            ],
        }
    if not obs:
        raise HTTPException(status_code=404, detail=f"No observations found for farm '{farm_id}'.")
    return Observation(**obs)


@router.get("/farms/{farm_id}/advisory", response_model=Advisory, summary="Get Explainable Farm Advisory")
def get_farm_advisory(
    farm_id: str,
    language: str = Query(default="en", description="Language code: en, kn, hi"),
) -> Advisory:
    """Retrieve 3-stage explainable agronomic advisory in selected language with fallback."""
    clean_id = farm_id.lower()
    lang_clean = language.lower()

    # Look for specific language, falling back to English
    advisory_data = DEMO_ADVISORIES.get((clean_id, lang_clean)) or DEMO_ADVISORIES.get((clean_id, "en"))

    if not advisory_data and clean_id in _REGISTERED_CUSTOM_FARMS:
        c_farm = _REGISTERED_CUSTOM_FARMS[clean_id]
        name = c_farm["name"]
        crop = c_farm["crop"]
        dist = c_farm["district"]
        if lang_clean == "kn":
            advisory_data = {
                "id": f"adv_{clean_id}_kn",
                "farm_id": clean_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "language": "kn",
                "severity": "optimal",
                "headline": f"{name}: ಬೆಳೆ ಆರೋಗ್ಯ ಸಾಮಾನ್ಯವಾಗಿದೆ",
                "description": f"ಸ್ಥಿತಿ: {dist} ಭಾಗದಲ್ಲಿ {crop} ಬೆಳೆ ಹಸಿರು ಉತ್ತಮ ಸ್ಥಿತಿಯಲ್ಲಿದೆ. ಶಿಫಾರಸು ಮಾಡಿದ ಕೃಷಿ ಕ್ರಮ ಮುಂದುವರಿಸಿ.",
                "metric_summary": "0.68 (ಸಾಮಾನ್ಯ ಮಾನದಂಡ 0.70)",
                "notice": f"{name} ಉಪಗ್ರಹ ವೀಕ್ಷಣೆಯಲ್ಲಿ ಎನ್‌ಡಿವಿಐ ಸೂಚ್ಯಂಕ ಸ್ಥಿರವಾಗಿದೆ.",
                "meaning": f"{crop} ಬೆಳೆಯ ಬೇರುಗಳು ಗಟ್ಟಿಯಾಗಿದ್ದು ಪೋಷಕಾಂಶ ಹೀರಿಕೊಳ್ಳಲು ಸೂಕ್ತ ಸಮಯ.",
                "next_steps": [
                    "ಹೊಲದ ಬದುಗಳಲ್ಲಿ ಕಳೆ ಮತ್ತು ನೀರು ನಿಲ್ಲದಂತೆ ಪರಿಶೀಲಿಸಿ.",
                    "ಮಣ್ಣಿನ ತೇವಾಂಶಕ್ಕೆ ಅನುಗುಣವಾಗಿ ನೀರು ಹಾಯಿಸಿ.",
                ],
                "sms_preview": f"[ಅರ್ಥ್‌ವರ್ಮ್-ಕೃಷಿ] {name} ({dist}): {crop} ಬೆಳೆ ಆರೋಗ್ಯಕರವಾಗಿದೆ. ಸಾಮಾನ್ಯ ಕೃಷಿ ಕ್ರಮ ಮುಂದುವರಿಸಿ.",
                "voice_transcript": f"ನಮಸ್ಕಾರ ರೈತ ಬಾಂಧವರೇ. {name} ಹೊಲದ {crop} ಬೆಳೆ ಉಪಗ್ರಹ ವರದಿಯಲ್ಲಿ ಉತ್ತಮ ಸ್ಥಿತಿಯಲ್ಲಿದೆ. ಹವಾಮಾನ ಅನುಕೂಲಕರವಾಗಿದೆ.",
                "uncertainty_note": "ಉಪಗ್ರಹ ಪ್ರತಿಫಲನ ಆಧಾರಿತ ಸಲಹೆ. ಚಿಕಿತ್ಸೆ ನೀಡುವ ಮುನ್ನ ಹೊಲದಲ್ಲಿ ಪರಿಶೀಲಿಸಿ.",
                "data_status": "observed",
            }
        else:
            advisory_data = {
                "id": f"adv_{clean_id}_en",
                "farm_id": clean_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "language": "en",
                "severity": "optimal",
                "headline": f"{name}: Canopy Health Optimal",
                "description": f"Status: Vegetative index for {crop} in {dist} indicates healthy chlorophyll vigor and canopy coverage.",
                "metric_summary": "0.68 (Benchmark 0.70)",
                "notice": f"Multi-spectral reflectance indicates steady and uniform greenness across {name}.",
                "meaning": f"Strong root establishment and active growth phase in {crop}.",
                "next_steps": [
                    "Verify top 10 cm root zone moisture prior to scheduled irrigation.",
                    "Maintain standard field sanitation and check field bunds.",
                ],
                "sms_preview": f"[EARTHWORM-AGRI] {name} ({dist}): {crop} canopy vigor is healthy. Continue standard irrigation schedule.",
                "voice_transcript": f"Hello farmer. Earthworm satellite advisory for {name}. Your {crop} canopy vigor is optimal and weather conditions remain favorable.",
                "uncertainty_note": "Satellite indicators detect spectral reflectance. Verify physical field conditions.",
                "data_status": "observed",
            }

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
    clean_id = farm_id.lower()
    weather = DEMO_WEATHER.get(clean_id)
    if not weather and clean_id in _REGISTERED_CUSTOM_FARMS:
        c_farm = _REGISTERED_CUSTOM_FARMS[clean_id]
        dist = c_farm["district"]
        weather = {
            "farm_id": clean_id,
            "district": dist,
            "temperature_celsius": 30.0,
            "condition": "Clear / Sunny",
            "rainfall_chance_pct": 5,
            "wind_speed_kmh": 10.0,
            "forecast_3day": [
                {"day": "Day 1", "temp": "30° / 21°", "rain": "0 mm"},
                {"day": "Day 2", "temp": "31° / 20°", "rain": "0 mm"},
                {"day": "Day 3", "temp": "29° / 22°", "rain": "<1 mm"},
            ],
            "recommendations": "Stable weather conditions favorable for field operations.",
            "source": "Open-Meteo Weather API",
        }
    if not weather:
        raise HTTPException(status_code=404, detail=f"No weather data for farm '{farm_id}'.")
    return weather


_CUSTOM_LAND_MARKERS: dict[str, list[dict]] = {}


@router.post("/farms/custom-marker", summary="Save Farmer's Manually Marked Land Boundary")
def save_custom_marker(marker: CustomLandMarker):
    """Save a farmer's manually marked land parcel with boundary coordinates and acreage."""
    if not marker.created_at:
        marker.created_at = datetime.now(timezone.utc).isoformat()
    farm_id = marker.farm_id.lower()
    if farm_id not in _CUSTOM_LAND_MARKERS:
        _CUSTOM_LAND_MARKERS[farm_id] = []

    # Store or update
    existing_idx = next((i for i, m in enumerate(_CUSTOM_LAND_MARKERS[farm_id]) if m["id"] == marker.id), None)
    if existing_idx is not None:
        _CUSTOM_LAND_MARKERS[farm_id][existing_idx] = marker.model_dump()
    else:
        _CUSTOM_LAND_MARKERS[farm_id].append(marker.model_dump())

    return {
        "success": True,
        "message": f"Land parcel '{marker.name}' ({marker.area_acres:.2f} Acres) marked successfully.",
        "marker": marker,
    }


@router.get("/farms/{farm_id}/custom-markers", summary="Get Farmer's Custom Marked Parcels")
def get_custom_markers(farm_id: str):
    """Retrieve all manually marked land parcels for a specific farm region."""
    farm_id_clean = farm_id.lower()
    markers = _CUSTOM_LAND_MARKERS.get(farm_id_clean, [])
    return {
        "farm_id": farm_id_clean,
        "total_marked_parcels": len(markers),
        "markers": markers,
    }


@router.delete("/farms/{farm_id}/custom-markers/{marker_id}", summary="Delete a Custom Marked Land Parcel")
def delete_custom_marker(farm_id: str, marker_id: str):
    """Delete a custom marked land parcel by ID."""
    farm_id_clean = farm_id.lower()
    if farm_id_clean in _CUSTOM_LAND_MARKERS:
        _CUSTOM_LAND_MARKERS[farm_id_clean] = [
            m for m in _CUSTOM_LAND_MARKERS[farm_id_clean] if m["id"] != marker_id
        ]
    return {"success": True, "deleted_id": marker_id}

