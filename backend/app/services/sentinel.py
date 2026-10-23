"""Copernicus Sentinel-2 client and live Process API integration.

Provides live satellite imagery retrieval and vegetation index processing
via Sentinel Hub with non-blocking fallback to local cached assets.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

# Bounding boxes for demo parcels [min_lon, min_lat, max_lon, max_lat]
FARM_BBOXES: Dict[str, Tuple[float, float, float, float]] = {
    "mandya": (76.85, 12.48, 76.92, 12.55),
    "ludhiana": (75.80, 30.85, 75.92, 30.95),
    "varanasi": (82.95, 25.28, 83.05, 25.38),
    "nashik": (73.75, 19.95, 73.88, 20.08),
}

# Regional metadata details for live dynamic view
FARM_METADATA: Dict[str, Dict[str, Any]] = {
    "mandya": {
        "region_name": "Mandya, Karnataka",
        "parcel_id": "Plot #142/A",
        "crop": "Sona Masoori Paddy (Panicle Initiation)",
        "coordinates": {"lat": 12.518, "lon": 76.885, "formatted": "12°31'05\" N, 76°53'06\" E"},
        "satellite": "Copernicus Sentinel-2B (MSI Level-2A)",
        "orbit": "Relative Orbit R019 • Altitude 786 km",
        "gsd": "10-meter Ground Sampling Distance",
        "latest_pass": "24 Feb 2024 • 10:48 UTC (Cloud-free 0.8%)",
        "solar_zenith": "28.4°",
        "mean_ndvi": 0.58,
        "baseline_ndvi": 0.70,
        "stress_level": "Moderate Moisture Stress (-17%)",
        "polygon_points": "125,45 285,35 305,135 145,150",
    },
    "ludhiana": {
        "region_name": "Ludhiana, Punjab",
        "parcel_id": "Plot #89/C",
        "crop": "PBW 343 Wheat (Active Tillering)",
        "coordinates": {"lat": 30.901, "lon": 75.857, "formatted": "30°54'04\" N, 75°51'25\" E"},
        "satellite": "Copernicus Sentinel-2A (MSI Level-2A)",
        "orbit": "Relative Orbit R076 • Altitude 786 km",
        "gsd": "10-meter Ground Sampling Distance",
        "latest_pass": "22 Feb 2024 • 11:05 UTC (Cloud-free 1.4%)",
        "solar_zenith": "42.1°",
        "mean_ndvi": 0.72,
        "baseline_ndvi": 0.68,
        "stress_level": "Optimal Vegetative Vigor (+6%)",
        "polygon_points": "100,55 310,40 290,165 90,145",
    },
    "varanasi": {
        "region_name": "Varanasi, Uttar Pradesh",
        "parcel_id": "Plot #214/B",
        "crop": "Varuna Mustard & Vegetables (Flowering)",
        "coordinates": {"lat": 25.330, "lon": 83.002, "formatted": "25°19'48\" N, 83°00'07\" E"},
        "satellite": "Copernicus Sentinel-2B (MSI Level-2A)",
        "orbit": "Relative Orbit R033 • Altitude 786 km",
        "gsd": "10-meter Ground Sampling Distance",
        "latest_pass": "23 Feb 2024 • 10:32 UTC (Cloud-free 2.1%)",
        "solar_zenith": "35.8°",
        "mean_ndvi": 0.64,
        "baseline_ndvi": 0.65,
        "stress_level": "Normal Physiological Growth (0%)",
        "polygon_points": "110,65 295,45 320,155 120,175",
    },
    "nashik": {
        "region_name": "Nashik, Maharashtra",
        "parcel_id": "Plot #56/D",
        "crop": "Red Pinhead Onion (Bulb Expansion)",
        "coordinates": {"lat": 20.015, "lon": 73.815, "formatted": "20°00'54\" N, 73°48'54\" E"},
        "satellite": "Copernicus Sentinel-2A (MSI Level-2A)",
        "orbit": "Relative Orbit R119 • Altitude 786 km",
        "gsd": "10-meter Ground Sampling Distance",
        "latest_pass": "21 Feb 2024 • 10:52 UTC (Cloud-free 0.4%)",
        "solar_zenith": "32.6°",
        "mean_ndvi": 0.61,
        "baseline_ndvi": 0.62,
        "stress_level": "Good Canopy Density (-2%)",
        "polygon_points": "130,50 300,60 280,180 115,160",
    },
}

# Evalscript: True-Color Natural RGB (B04 Red, B03 Green, B02 Blue)
TRUE_COLOR_EVALSCRIPT = """//VERSION=3
function setup() {
  return {
    input: ["B04", "B03", "B02"],
    output: { bands: 3 }
  };
}
function evaluatePixel(sample) {
  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
}
"""

# Evalscript: NDVI False-Color Heatmap (Normalized Difference Vegetation Index)
NDVI_EVALSCRIPT = """//VERSION=3
function setup() {
  return {
    input: ["B04", "B08"],
    output: { bands: 3 }
  };
}
function evaluatePixel(sample) {
  let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04 + 0.0001);
  return colorBlend(ndvi, [-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0], [
    [0.1, 0.1, 0.5], // water/shadow
    [0.7, 0.7, 0.7], // bare soil
    [0.9, 0.8, 0.2], // sparse / dry
    [0.9, 0.6, 0.1], // low vigor
    [0.6, 0.8, 0.2], // moderate vigor
    [0.2, 0.7, 0.2], // healthy crop
    [0.0, 0.5, 0.1]  // dense lush canopy
  ]);
}
"""

# Evalscript: Color Infrared / False Color (B08 NIR, B04 Red, B03 Green)
FALSE_COLOR_EVALSCRIPT = """//VERSION=3
function setup() {
  return {
    input: ["B08", "B04", "B03"],
    output: { bands: 3 }
  };
}
function evaluatePixel(sample) {
  return [2.5 * sample.B08, 2.5 * sample.B04, 2.5 * sample.B03];
}
"""

# Evalscript: NDMI Normalized Difference Moisture Index (B08 NIR, B11 SWIR)
MOISTURE_EVALSCRIPT = """//VERSION=3
function setup() {
  return {
    input: ["B08", "B11"],
    output: { bands: 3 }
  };
}
function evaluatePixel(sample) {
  let ndmi = (sample.B08 - sample.B11) / (sample.B08 + sample.B11 + 0.0001);
  return colorBlend(ndmi, [-0.6, -0.2, 0.0, 0.2, 0.4, 0.6], [
    [0.8, 0.2, 0.0], // dry soil / extreme deficit
    [0.9, 0.6, 0.2], // moisture stress
    [0.9, 0.9, 0.5], // low moisture
    [0.4, 0.7, 0.9], // adequate moisture
    [0.1, 0.4, 0.8], // high canopy hydration
    [0.0, 0.1, 0.6]  // water body / saturated
  ]);
}
"""

EVALSCRIPTS: Dict[str, str] = {
    "true-color": TRUE_COLOR_EVALSCRIPT,
    "ndvi": NDVI_EVALSCRIPT,
    "false-color": FALSE_COLOR_EVALSCRIPT,
    "moisture": MOISTURE_EVALSCRIPT,
}


class SentinelService:
    """Manages authentication, caching, and Process API queries for Sentinel-2."""

    def __init__(self) -> None:
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0.0
        self._image_cache: Dict[str, bytes] = {}

    def is_configured(self) -> bool:
        """Return True if credentials are provided."""
        return settings.is_sentinel_configured

    def get_access_token(self, timeout: float = 10.0) -> Optional[str]:
        """Fetch or return cached OAuth2 Bearer token."""
        if not self.is_configured():
            return None

        # Return cached token if valid for at least another 60 seconds
        if self._access_token and time.time() < (self._token_expires_at - 60):
            return self._access_token

        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.post(
                    settings.sentinel_oauth_url,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": settings.sentinel_client_id,
                        "client_secret": settings.sentinel_client_secret,
                    },
                )

            if response.status_code == 200:
                data = response.json()
                self._access_token = data.get("access_token")
                expires_in = data.get("expires_in", 3600)
                self._token_expires_at = time.time() + expires_in
                logger.info("Successfully authenticated with Sentinel Hub.")
                return self._access_token
            else:
                logger.error(
                    "Sentinel authentication failed (HTTP %s): %s",
                    response.status_code,
                    response.text[:200],
                )
                return None
        except Exception as exc:
            logger.error("Sentinel Hub authentication error: %s", type(exc).__name__)
            return None

    def verify_connection(self) -> Dict[str, Any]:
        """Perform a safe read-only authentication check without exposing secrets."""
        if not self.is_configured():
            return {
                "configured": False,
                "connected": False,
                "status": "not_configured",
                "message": "Sentinel Hub credentials are not configured.",
            }

        token = self.get_access_token()
        if token:
            return {
                "configured": True,
                "connected": True,
                "status": "connected",
                "provider": "Copernicus Sentinel Hub (ESA)",
                "message": "Successfully authenticated with Sentinel Hub OAuth2 service.",
            }

        return {
            "configured": True,
            "connected": False,
            "status": "authentication_failed",
            "message": "Failed to authenticate with Sentinel Hub. Check SENTINEL_CLIENT_ID and SECRET.",
        }

    def get_farm_metadata(self, farm_id: str) -> Optional[Dict[str, Any]]:
        """Return satellite metadata and observation parameters for farm."""
        farm_key = farm_id.lower()
        meta = FARM_METADATA.get(farm_key)
        if not meta:
            return None
        return {
            **meta,
            "available_layers": list(EVALSCRIPTS.keys()),
            "is_live_connected": self.is_configured(),
        }

    def fetch_live_satellite_image(
        self,
        farm_id: str,
        layer: str = "true-color",
        width: int = 512,
        height: int = 320,
        timeout: float = 20.0,
    ) -> Optional[bytes]:
        """Query Sentinel Hub Process API for requested spectral layer."""
        farm_key = farm_id.lower()
        clean_layer = layer.lower().strip()
        if clean_layer not in EVALSCRIPTS:
            clean_layer = "true-color"

        cache_key = f"{farm_key}:{clean_layer}"
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]

        bbox = FARM_BBOXES.get(farm_key)
        token = self.get_access_token()
        evalscript = EVALSCRIPTS[clean_layer]

        if token and bbox:
            try:
                payload = {
                    "input": {
                        "bounds": {
                            "bbox": list(bbox),
                            "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
                        },
                        "data": [
                            {
                                "type": "sentinel-2-l2a",
                                "dataFilter": {
                                    "timeRange": {
                                        "from": "2024-01-01T00:00:00Z",
                                        "to": "2024-02-28T23:59:59Z",
                                    },
                                    "maxCloudCoverage": 30,
                                },
                            }
                        ],
                    },
                    "output": {
                        "width": width,
                        "height": height,
                        "responses": [
                            {
                                "identifier": "default",
                                "format": {"type": "image/jpeg"},
                            }
                        ],
                    },
                    "evalscript": evalscript,
                }

                with httpx.Client(timeout=timeout) as client:
                    resp = client.post(
                        settings.sentinel_process_url,
                        headers={
                            "Authorization": f"Bearer {token}",
                            "Accept": "image/jpeg",
                        },
                        json=payload,
                    )

                if resp.status_code == 200 and len(resp.content) > 1000:
                    logger.info("Successfully fetched live Sentinel-2 '%s' for farm '%s'.", clean_layer, farm_key)
                    self._image_cache[cache_key] = resp.content
                    return resp.content
                else:
                    logger.warning(
                        "Process API returned %s for farm '%s' layer '%s'. Falling back to local asset.",
                        resp.status_code,
                        farm_key,
                        clean_layer,
                    )
            except Exception as exc:
                logger.warning(
                    "Process API call failed for farm '%s' layer '%s' (%s). Falling back to local asset.",
                    farm_key,
                    clean_layer,
                    type(exc).__name__,
                )

        # Fallback to local asset
        return self._load_local_fallback(farm_key, clean_layer)

    def _load_local_fallback(self, farm_key: str, layer: str = "true-color") -> Optional[bytes]:
        """Load regional satellite image asset from local disk."""
        candidates = [
            Path(__file__).resolve().parent.parent.parent / "frontend" / "assets" / f"{farm_key}_{layer}.jpg",
            Path(__file__).resolve().parent.parent.parent / "frontend" / "assets" / f"{farm_key}.jpg",
            Path(__file__).resolve().parent.parent.parent.parent / "assets" / f"{farm_key}_{layer}.jpg",
            Path(__file__).resolve().parent.parent.parent.parent / "assets" / f"{farm_key}.jpg",
            Path.cwd() / "frontend" / "assets" / f"{farm_key}_{layer}.jpg",
            Path.cwd() / "frontend" / "assets" / f"{farm_key}.jpg",
            Path.cwd() / "assets" / f"{farm_key}_{layer}.jpg",
            Path.cwd() / "assets" / f"{farm_key}.jpg",
        ]
        for p in candidates:
            if p.is_file():
                try:
                    return p.read_bytes()
                except Exception:
                    pass
        return None


sentinel_service = SentinelService()
