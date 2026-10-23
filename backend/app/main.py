"""Main FastAPI application entrypoint for Earthworm Advisory Backend."""

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import farms, health
from app.config import settings


def _find_frontend_dir() -> Path:
    candidates = [
        Path(__file__).resolve().parent.parent.parent / "frontend",
        Path(__file__).resolve().parent.parent.parent / "Frontend",
        Path(__file__).resolve().parent.parent / "frontend",
        Path(__file__).resolve().parent.parent / "Frontend",
        Path.cwd() / "frontend",
        Path.cwd() / "Frontend",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return candidates[0]


_FRONTEND_DIR = _find_frontend_dir()


def _get_frontend_html() -> str:
    search_paths = [
        _FRONTEND_DIR / "index.html",
        _FRONTEND_DIR / "code.html",
        Path(__file__).resolve().parent.parent.parent / "frontend" / "index.html",
        Path(__file__).resolve().parent.parent.parent / "frontend" / "code.html",
        Path(__file__).resolve().parent.parent.parent / "index.html",
        Path(__file__).resolve().parent.parent / "frontend" / "index.html",
        Path(__file__).resolve().parent.parent / "frontend" / "code.html",
        Path(__file__).resolve().parent.parent / "index.html",
        Path.cwd() / "frontend" / "index.html",
        Path.cwd() / "index.html",
    ]
    for p in search_paths:
        if p.is_file():
            try:
                return p.read_text(encoding="utf-8")
            except Exception:
                pass
    return ""


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
            name="frontend_app",
        )
        application.mount(
            "/frontend",
            StaticFiles(directory=str(_FRONTEND_DIR), html=True),
            name="frontend_static",
        )

    @application.get("/index.html", include_in_schema=False)
    @application.get("/code.html", include_in_schema=False)
    def serve_html():
        html_text = _get_frontend_html()
        if html_text:
            return HTMLResponse(content=html_text, status_code=200)
        return JSONResponse(status_code=404, content={"error": "Not Found"})

    @application.get("/", tags=["Root"])
    def root(request: Request, format: str | None = None):
        accept = request.headers.get("accept", "")
        # If client explicitly requests json or test client / curl without text/html
        if format == "json" or ("application/json" in accept and "text/html" not in accept) or ("text/html" not in accept):
            return {
                "app": settings.app_name,
                "version": "0.1.0",
                "docs_url": "/docs",
                "health_url": f"{settings.api_prefix}/health",
                "app_url": "/app/code.html",
            }

        # Otherwise serve the interactive Earthworm dashboard to web browsers
        html_text = _get_frontend_html()
        if html_text:
            return HTMLResponse(content=html_text, status_code=200)

        return {
            "app": settings.app_name,
            "version": "0.1.0",
            "docs_url": "/docs",
            "health_url": f"{settings.api_prefix}/health",
            "app_url": "/app/code.html",
        }

    return application


app = create_app()

