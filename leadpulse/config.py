"""LeadPulse AI — Application configuration via environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration loaded from environment / .env file."""

    # ── Database ──────────────────────────────────────────────────────
    # Defaults to local SQLite; override with postgresql+asyncpg in production/docker
    DATABASE_URL: str = "sqlite+aiosqlite:///./leadpulse.db"

    # ── Meta / WhatsApp ───────────────────────────────────────────────
    META_VERIFY_TOKEN: str = ""
    META_APP_SECRET: str = ""  # HMAC verification of webhook payloads

    # ── AI ────────────────────────────────────────────────────────────
    CLAUDE_API_KEY: str = ""  # Default key; tenants may override with their own

    # ── Email (Resend) ────────────────────────────────────────────────
    RESEND_API_KEY: str = ""

    # ── Telegram alerts ───────────────────────────────────────────────
    TELEGRAM_BOT_TOKEN: str = ""

    # ── JWT auth ──────────────────────────────────────────────────────
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 1440  # 24 hours

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
