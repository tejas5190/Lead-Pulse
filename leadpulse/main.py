"""LeadPulse AI — FastAPI application entry-point."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import Base, engine


# ── Stub routers (populated by other swarm agents) ────────────────────
# Import the real routers once they exist; fall back to empty placeholders
# so the app can start before the route files are written.

try:
    from .routes.webhook import router as webhook_router
except ImportError:  # pragma: no cover
    from fastapi import APIRouter
    webhook_router = APIRouter(prefix="/webhook", tags=["webhook"])

try:
    from .routes.dashboard import router as dashboard_router
except ImportError:  # pragma: no cover
    from fastapi import APIRouter
    dashboard_router = APIRouter(prefix="/dashboard", tags=["dashboard"])

try:
    from .routes.auth import router as auth_router
except ImportError:  # pragma: no cover
    from fastapi import APIRouter
    auth_router = APIRouter(prefix="/auth", tags=["auth"])


# ── Lifespan ──────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Create DB tables on startup; seed demo tenant; dispose engine on shutdown."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        from .database import Tenant, async_session_factory
        from .auth import DEMO_TENANT_ID, hash_password
        async with async_session_factory() as session:
            existing = await session.get(Tenant, DEMO_TENANT_ID)
            if not existing:
                demo_tenant = Tenant(
                    id=DEMO_TENANT_ID,
                    company_name="LeadPulse Demo Client",
                    industry="universal",
                    owner_email="demo@leadpulse.ai",
                    hashed_password=hash_password("demo1234"),
                )
                session.add(demo_tenant)
                await session.commit()
    except Exception:
        pass
    yield
    await engine.dispose()


# ── App ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="LeadPulse AI",
    description="Multi-tenant Meta Ads lead qualification via WhatsApp AI",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — wide-open for development; tighten in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────

app.include_router(webhook_router)
app.include_router(dashboard_router)
app.include_router(auth_router)

# ── Static Dashboard Mount ─────────────────────────────────────────────

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def serve_dashboard():
    """Serve the frontend dashboard single-page app."""
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "ok", "message": "LeadPulse AI API is running"}


# ── Health check ──────────────────────────────────────────────────────


@app.get("/health", tags=["infra"])
async def health_check() -> dict:
    """Simple liveness probe."""
    return {"status": "ok", "service": "leadpulse-ai"}
