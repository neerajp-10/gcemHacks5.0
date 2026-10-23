"""Health check endpoint for the Earthworm Advisory Backend."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.db.supabase import is_supabase_configured, verify_supabase_connection

router = APIRouter()


class DatabaseHealthResponse(BaseModel):
    """Structured response for database health and connectivity."""

    configured: bool
    connected: bool
    status: str
    message: str
    host: Optional[str] = None


class HealthResponse(BaseModel):
    """Structured response model for service health check."""

    status: str = Field(..., description="Overall service status (e.g., 'healthy')")
    app: str = Field(..., description="Application name")
    environment: str = Field(..., description="Current deployment environment")
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp of the check")
    data_mode: str = Field(..., description="Current operational data mode ('demo_ready', 'live')")
    supabase_configured: bool = Field(default=False, description="Whether Supabase credentials are configured")


@router.get("/health", response_model=HealthResponse, summary="Service Health Check")
def get_health() -> HealthResponse:
    """Return current service health and operational status."""
    return HealthResponse(
        status="healthy",
        app="Earthworm Advisory Backend",
        environment="development",
        timestamp=datetime.now(timezone.utc).isoformat(),
        data_mode="live" if is_supabase_configured() else "demo_ready",
        supabase_configured=is_supabase_configured(),
    )


@router.get("/health/db", response_model=DatabaseHealthResponse, summary="Supabase Connection Verification")
def get_database_health() -> DatabaseHealthResponse:
    """Run a safe, read-only connection check against Supabase."""
    result = verify_supabase_connection()
    return DatabaseHealthResponse(**result)
