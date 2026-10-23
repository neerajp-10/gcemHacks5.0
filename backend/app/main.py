"""Main FastAPI application entrypoint for Earthworm Advisory Backend."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pathlib import Path
from fastapi.staticfiles import StaticFiles
from app.api.routes import farms, health
from app.config import settings

_FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "Frontend"


def create_app() -> FastAPI:
    """Factory creating and configuring the FastAPI application."""
    application = FastAPI(
        title=settings.app_name,
        description=(
            "Satellite-based early-warning and crop advisory backend for "
            "smallholder paddy farmers in Mandya, Karnataka, India."
        ),
        version="0.1.0",
        debug=settings.debug,
    )

    # Cross-Origin Resource Sharing (CORS) setup for local development
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global structured error handler
    @application.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred.",
                "path": str(request.url.path),
            },
        )

    # Register API routers
    application.include_router(
        health.router,
        prefix=settings.api_prefix,
        tags=["Health"],
    )
    application.include_router(
        farms.router,
        prefix=settings.api_prefix,
        tags=["Farms"],
    )

    # Mount Frontend UI static files if present
    if _FRONTEND_DIR.exists():
        application.mount(
            "/app",
            StaticFiles(directory=str(_FRONTEND_DIR), html=True),
            name="frontend",
        )

    @application.get("/", tags=["Root"])
    def root():
        return {
            "app": settings.app_name,
            "version": "0.1.0",
            "docs_url": "/docs",
            "health_url": f"{settings.api_prefix}/health",
            "app_url": "/app/code.html",
        }

    return application


app = create_app()
