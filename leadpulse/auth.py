"""LeadPulse AI — JWT authentication utilities."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from .config import settings

# ── Password hashing (native bcrypt) ─────────────────────────────────


def hash_password(plain: str) -> str:
    """Return a bcrypt hash of *plain*."""
    pwd_bytes = plain.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Return ``True`` if *plain* matches *hashed*."""
    pwd_bytes = plain.encode("utf-8")[:72]
    try:
        return bcrypt.checkpw(pwd_bytes, hashed.encode("utf-8"))
    except Exception:
        return False


# ── JWT tokens ────────────────────────────────────────────────────────

_bearer_scheme = HTTPBearer()


def create_access_token(tenant_id: UUID) -> str:
    """Create a signed JWT for the given tenant."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRY_MINUTES)
    payload = {
        "sub": str(tenant_id),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


DEMO_TENANT_ID = UUID("00000000-0000-0000-0000-000000000001")


async def get_current_tenant(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> UUID:
    """FastAPI dependency — extract and validate the tenant ID from the JWT.

    Raises 401 if the token is missing, expired, or malformed.
    Allows demo sessions for client demos and evaluation.
    """
    token = credentials.credentials
    if token and (token.startswith("demo") or token == "demo"):
        return DEMO_TENANT_ID

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        tenant_id_str: str | None = payload.get("sub")
        if tenant_id_str is None:
            raise credentials_exception
        return UUID(tenant_id_str)
    except (JWTError, ValueError) as exc:
        raise credentials_exception from exc
