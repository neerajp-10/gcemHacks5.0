"""Reusable backend-only Supabase client and connection verification.

Provides safe access to Supabase with non-blocking fallbacks when
credentials are not yet configured.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import httpx
from supabase import Client, create_client

from app.config import settings

logger = logging.getLogger(__name__)

# Cached singleton client instance
_supabase_client: Optional[Client] = None
_client_initialized: bool = False


def is_supabase_configured() -> bool:
    """Check whether Supabase environment variables are provided.

    Returns True only if both SUPABASE_URL and SUPABASE_SECRET_KEY
    are non-empty and not default sample placeholders.
    """
    url = (settings.supabase_url or "").strip()
    key = (settings.effective_supabase_key or "").strip()

    if not url or not key:
        return False

    # Ignore default sample placeholders from .env.example
    if "your-project-ref" in url or "your-supabase" in key:
        return False

    return True


def get_supabase_client() -> Optional[Client]:
    """Retrieve or initialize the reusable Supabase client.

    Returns None safely if credentials are absent or invalid, allowing
    the application to remain fully functional in demo mode.
    """
    global _supabase_client, _client_initialized

    if _client_initialized:
        return _supabase_client

    if not is_supabase_configured():
        logger.info("Supabase is not configured; running in demo mode.")
        _supabase_client = None
        _client_initialized = True
        return None

    try:
        url = settings.supabase_url.strip()
        key = settings.effective_supabase_key.strip()
        _supabase_client = create_client(url, key)
        _client_initialized = True
        logger.info("Supabase client initialized successfully.")
        return _supabase_client
    except Exception as exc:
        logger.error("Failed to initialize Supabase client: %s", type(exc).__name__)
        _supabase_client = None
        _client_initialized = True
        return None


def reset_supabase_client() -> None:
    """Reset cached client state for dynamic testing or reload."""
    global _supabase_client, _client_initialized
    _supabase_client = None
    _client_initialized = False


def verify_supabase_connection(timeout: float = 4.0) -> Dict[str, Any]:
    """Verify Supabase connection safely without modifying data or exposing secrets.

    Performs a non-destructive, read-only check against the PostgREST root.
    Never exposes API keys or raw tokens in responses or logs.
    """
    if not is_supabase_configured():
        return {
            "configured": False,
            "connected": False,
            "status": "not_configured",
            "message": "Supabase credentials are not configured. Running in demo mode.",
            "host": None,
        }

    url = settings.supabase_url.strip()
    key = settings.effective_supabase_key.strip()

    # Extract safe host name for reporting without exposing credentials
    try:
        parsed = urlparse(url)
        safe_host = parsed.netloc or "unknown"
    except Exception:
        safe_host = "invalid_url"

    client = get_supabase_client()
    if client is None:
        return {
            "configured": True,
            "connected": False,
            "status": "initialization_failed",
            "message": "Failed to initialize Supabase client.",
            "host": safe_host,
        }

    # Safe read-only probe: PostgREST root returns OpenAPI spec (HTTP 200) when authenticated
    endpoint = f"{url.rstrip('/')}/rest/v1/"
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
    }

    try:
        with httpx.Client(timeout=timeout) as http_client:
            response = http_client.get(endpoint, headers=headers)

        if response.status_code == 200:
            return {
                "configured": True,
                "connected": True,
                "status": "connected",
                "message": "Successfully connected and authenticated with Supabase PostgREST.",
                "host": safe_host,
            }
        elif response.status_code in (401, 403):
            return {
                "configured": True,
                "connected": False,
                "status": "authentication_failed",
                "message": "Supabase authentication failed. Check SUPABASE_SECRET_KEY.",
                "host": safe_host,
            }
        else:
            return {
                "configured": True,
                "connected": False,
                "status": "unexpected_status",
                "message": f"Received unexpected response (HTTP {response.status_code}) from Supabase.",
                "host": safe_host,
            }

    except httpx.ConnectError:
        return {
            "configured": True,
            "connected": False,
            "status": "connection_error",
            "message": "Could not connect to Supabase host. Verify SUPABASE_URL and network connectivity.",
            "host": safe_host,
        }
    except httpx.TimeoutException:
        return {
            "configured": True,
            "connected": False,
            "status": "timeout",
            "message": f"Connection to Supabase timed out after {timeout} seconds.",
            "host": safe_host,
        }
    except Exception as exc:
        return {
            "configured": True,
            "connected": False,
            "status": "error",
            "message": f"Connection check encountered an error: {type(exc).__name__}",
            "host": safe_host,
        }
