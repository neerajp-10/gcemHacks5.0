"""Vercel Serverless Function entrypoint for Earthworm FastAPI application."""

import sys
from pathlib import Path

# Add backend and parent directories to sys.path so app modules import cleanly
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
backend_candidate = parent_dir / "backend"

for p in [backend_candidate, parent_dir, current_dir]:
    if p.is_dir() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

from app.main import app

# Vercel's Python runtime discovers 'app' as the ASGI application

