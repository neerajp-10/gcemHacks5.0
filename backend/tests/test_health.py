"""Tests for the health check endpoint and application error handling."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Root endpoint returns application metadata and links."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "Earthworm Advisory Backend"
    assert "health_url" in data


def test_health_check_returns_200():
    """GET /api/health returns 200 OK and expected structure."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "Earthworm Advisory Backend"
    assert data["environment"] == "development"
    assert data["data_mode"] in ("demo_ready", "live")
    assert "timestamp" in data


def test_health_check_timestamp_format():
    """Verify timestamp is present and parseable."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    timestamp = data["timestamp"]
    assert "T" in timestamp


def test_unknown_route_returns_404():
    """Verify 404 response for unknown routes."""
    response = client.get("/api/non-existent-endpoint")
    assert response.status_code == 404
