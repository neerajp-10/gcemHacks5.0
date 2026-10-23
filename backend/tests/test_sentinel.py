"""Tests for live Copernicus Sentinel Hub integration and satellite imagery endpoints."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_sentinel_health_endpoint():
    """GET /api/health/sentinel returns Sentinel Hub connectivity status."""
    response = client.get("/api/health/sentinel")
    assert response.status_code == 200
    data = response.json()
    assert data["configured"] is True
    assert data["connected"] is True
    assert data["status"] == "connected"


def test_farm_satellite_image_endpoint():
    """GET /api/farms/{id}/satellite-image returns JPEG imagery."""
    response = client.get("/api/farms/mandya/satellite-image")
    assert response.status_code == 200
    assert response.headers.get("content-type") == "image/jpeg"
    assert len(response.content) > 1000


def test_farm_listing_includes_satellite_image_url():
    """Verify that farms returned by /api/farms contain satellite_image_url."""
    response = client.get("/api/farms")
    assert response.status_code == 200
    farms = response.json()
    for farm in farms:
        assert "satellite_image_url" in farm
        assert farm["satellite_image_url"].startswith("/api/farms/")
