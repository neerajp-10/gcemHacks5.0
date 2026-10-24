"""Tests for farm, observation, advisory, and weather endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_farms():
    """GET /api/farms returns the 4 pan-India demo parcels."""
    response = client.get("/api/farms")
    assert response.status_code == 200
    farms = response.json()
    assert len(farms) == 4
    farm_ids = [f["id"] for f in farms]
    assert "mandya" in farm_ids
    assert "ludhiana" in farm_ids


def test_get_specific_farm():
    """GET /api/farms/{id} returns details for a valid farm."""
    response = client.get("/api/farms/mandya")
    assert response.status_code == 200
    data = response.json()
    assert data["district"] == "Mandya"
    assert data["state"] == "Karnataka"
    assert data["crop"] == "Paddy"


def test_get_unknown_farm_returns_404():
    """Unknown farm returns 404."""
    response = client.get("/api/farms/nonexistent_farm")
    assert response.status_code == 404


def test_get_observations():
    """GET /api/farms/{id}/observations returns NDVI and time series."""
    response = client.get("/api/farms/mandya/observations")
    assert response.status_code == 200
    data = response.json()
    assert data["metric"] == "NDVI"
    assert data["value"] == 0.58
    assert len(data["history"]) >= 3
    assert data["status"] == "demo"


def test_get_advisory_english():
    """GET /api/farms/{id}/advisory defaults to English."""
    response = client.get("/api/farms/mandya/advisory?language=en")
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "en"
    assert "notice" in data
    assert "meaning" in data
    assert len(data["next_steps"]) > 0


def test_get_advisory_kannada():
    """GET /api/farms/{id}/advisory?language=kn returns localized Kannada content."""
    response = client.get("/api/farms/mandya/advisory?language=kn")
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "kn"
    assert "ತೇವಾಂಶ" in data["headline"] or "ಮಂಡ್ಯ" in data["notice"]


def test_get_communication_preview_sms():
    """GET /api/farms/{id}/communications/preview returns SMS preview with character count."""
    response = client.get("/api/farms/mandya/communications/preview?channel=sms&language=en")
    assert response.status_code == 200
    data = response.json()
    assert data["channel"] == "sms"
    assert data["status"] == "preview_only"
    assert len(data["preview_text"]) > 0
    assert data["char_count"] == len(data["preview_text"])


def test_get_weather():
    """GET /api/farms/{id}/weather returns 3-day forecast."""
    response = client.get("/api/farms/mandya/weather")
    assert response.status_code == 200
    data = response.json()
    assert "days" in data
    assert len(data["days"]) == 3


def test_custom_land_marker_lifecycle():
    """Verify farmers can save, retrieve, and delete custom land markers."""
    payload = {
        "id": "plot_test_123",
        "farm_id": "mandya",
        "name": "Kavitha Sugarcane Plot",
        "crop": "Sugarcane",
        "points": [
            {"lat": 12.518, "lng": 76.888},
            {"lat": 12.519, "lng": 76.888},
            {"lat": 12.519, "lng": 76.889},
            {"lat": 12.518, "lng": 76.889},
        ],
        "area_acres": 1.45,
        "area_hectares": 0.59,
        "centroid": {"lat": 12.5185, "lng": 76.8885},
        "created_at": "2026-10-24T06:00:00Z",
        "notes": "Boundary along north irrigation canal",
    }
    # 1. Save marker
    res_save = client.post("/api/farms/custom-marker", json=payload)
    assert res_save.status_code == 200
    assert res_save.json()["success"] is True

    # 2. Retrieve markers for farm
    res_get = client.get("/api/farms/mandya/custom-markers")
    assert res_get.status_code == 200
    data_get = res_get.json()
    assert data_get["total_marked_parcels"] >= 1
    assert any(m["id"] == "plot_test_123" for m in data_get["markers"])

    # 3. Delete marker
    res_del = client.delete("/api/farms/mandya/custom-markers/plot_test_123")
    assert res_del.status_code == 200
    assert res_del.json()["success"] is True

