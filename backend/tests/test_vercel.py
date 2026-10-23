"""Tests verifying Vercel serverless entrypoint and routing compatibility."""

import sys
from pathlib import Path

# Ensure repo root is in sys.path when running pytest from backend/
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from fastapi.testclient import TestClient
from api.index import app

client = TestClient(app)


def test_vercel_entrypoint_health():
    """Verify that Vercel entrypoint responds on /api/health."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_vercel_entrypoint_farms():
    """Verify that Vercel entrypoint serves farm routes."""
    response = client.get("/api/farms")
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_vercel_entrypoint_kannada_advisory():
    """Verify that Vercel entrypoint serves localized Kannada advisory."""
    response = client.get("/api/farms/mandya/advisory?language=kn")
    assert response.status_code == 200
    assert response.json()["language"] == "kn"
