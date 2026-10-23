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

# Evalscript for True-Color Sentinel-2 Level-2A imagery
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

    def fetch_live_satellite_image(
        self,
        farm_id: str,
        width: int = 512,
        height: int = 320,
        timeout: float = 20.0,
    ) -> Optional[bytes]:
        """Query Sentinel Hub Process API for true-color satellite imagery."""
        farm_key = farm_id.lower()
        if farm_key in self._image_cache:
            return self._image_cache[farm_key]

        bbox = FARM_BBOXES.get(farm_key)
        token = self.get_access_token()

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
                    "evalscript": TRUE_COLOR_EVALSCRIPT,
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
                    logger.info("Successfully fetched live Sentinel-2 image for farm '%s'.", farm_key)
                    self._image_cache[farm_key] = resp.content
                    return resp.content
                else:
                    logger.warning(
                        "Process API returned %s for farm '%s'. Falling back to local asset.",
                        resp.status_code,
                        farm_key,
                    )
            except Exception as exc:
                logger.warning(
                    "Process API call failed for farm '%s' (%s). Falling back to local asset.",
                    farm_key,
                    type(exc).__name__,
                )

        # Fallback to local asset
        return self._load_local_fallback(farm_key)

    def _load_local_fallback(self, farm_key: str) -> Optional[bytes]:
        """Load regional satellite image asset from local disk."""
        candidates = [
            Path(__file__).resolve().parent.parent.parent / "frontend" / "assets" / f"{farm_key}.jpg",
            Path(__file__).resolve().parent.parent.parent.parent / "assets" / f"{farm_key}.jpg",
            Path(__file__).resolve().parent.parent.parent.parent / "frontend" / "assets" / f"{farm_key}.jpg",
            Path.cwd() / "frontend" / "assets" / f"{farm_key}.jpg",
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
