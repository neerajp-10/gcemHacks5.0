"""Application configuration settings for Earthworm backend.

Safe defaults are provided so the application runs out of the box
without requiring any .env file or external service credentials.
"""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application runtime settings."""

    app_name: str = "Earthworm Advisory Backend"
    app_env: str = "development"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    api_prefix: str = "/api"

    # Optional provider and database credentials (safe defaults when absent)
    supabase_url: Optional[str] = None
    supabase_secret_key: Optional[str] = None
    supabase_key: Optional[str] = None  # fallback alias

    # Optional Copernicus Sentinel Hub Credentials
    sentinel_client_id: Optional[str] = None
    sentinel_client_secret: Optional[str] = None
    sentinel_oauth_url: str = "https://services.sentinel-hub.com/oauth/token"
    sentinel_process_url: str = "https://services.sentinel-hub.com/api/v1/process"

    @property
    def effective_supabase_key(self) -> Optional[str]:
        """Return the configured Supabase secret key, checking aliases."""
        return self.supabase_secret_key or self.supabase_key

    @property
    def is_sentinel_configured(self) -> bool:
        """Return True if Sentinel client credentials are provided."""
        return bool(
            self.sentinel_client_id
            and self.sentinel_client_secret
            and "your-" not in self.sentinel_client_id
        )


    model_config = SettingsConfigDict(
        env_file=(_BACKEND_DIR / ".env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
