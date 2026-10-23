"""Tests for backend-only Supabase client and connection verification."""

from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.db.supabase import (
    get_supabase_client,
    is_supabase_configured,
    reset_supabase_client,
    verify_supabase_connection,
)
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_supabase_state():
    """Ensure cached Supabase client is reset before each test."""
    reset_supabase_client()
    yield
    reset_supabase_client()


def test_supabase_unconfigured_by_default():
    """When credentials are absent or default placeholders, report unconfigured."""
    with patch.object(settings, "supabase_url", None), patch.object(settings, "supabase_secret_key", None), patch.object(settings, "supabase_key", None):
        reset_supabase_client()
        assert is_supabase_configured() is False
        assert get_supabase_client() is None

        result = verify_supabase_connection()
        assert result["configured"] is False
        assert result["connected"] is False
        assert result["status"] == "not_configured"
        assert "demo mode" in result["message"]


def test_health_db_endpoint_unconfigured():
    """GET /api/health/db returns 200 with unconfigured status when credentials absent."""
    with patch.object(settings, "supabase_url", None), patch.object(settings, "supabase_secret_key", None), patch.object(settings, "supabase_key", None):
        reset_supabase_client()
        response = client.get("/api/health/db")
        assert response.status_code == 200
        data = response.json()
        assert data["configured"] is False
        assert data["connected"] is False
        assert data["status"] == "not_configured"


def test_verify_connection_never_exposes_secret_key():
    """Ensure secret key is never leaked in verification response."""
    secret = "super-secret-service-role-key-998877"
    with patch.object(settings, "supabase_url", "https://xyzexample.supabase.co"), patch.object(settings, "supabase_secret_key", secret):
        reset_supabase_client()
        result = verify_supabase_connection(timeout=0.5)

        # Check all string values in result dictionary
        result_text = str(result)
        assert secret not in result_text
        assert "xyzexample.supabase.co" in result.get("host", "")


def test_verify_connection_success_mocked():
    """When PostgREST responds 200, report successful connection."""
    with patch.object(settings, "supabase_url", "https://mockproject.supabase.co"), patch.object(settings, "supabase_secret_key", "mock-key"):
        reset_supabase_client()
        mock_response = MagicMock(status_code=200)

        with patch("httpx.Client.get", return_value=mock_response):
            result = verify_supabase_connection()
            assert result["configured"] is True
            assert result["connected"] is True
            assert result["status"] == "connected"


def test_verify_connection_auth_failure_mocked():
    """When PostgREST responds 401, report authentication failure safely."""
    with patch.object(settings, "supabase_url", "https://mockproject.supabase.co"), patch.object(settings, "supabase_secret_key", "invalid-key"):
        reset_supabase_client()
        mock_response = MagicMock(status_code=401)

        with patch("httpx.Client.get", return_value=mock_response):
            result = verify_supabase_connection()
            assert result["configured"] is True
            assert result["connected"] is False
            assert result["status"] == "authentication_failed"
