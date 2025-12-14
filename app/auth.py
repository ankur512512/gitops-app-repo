from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.settings import settings

DEMO_USER = {
    "username": "admin",
    "password": "admin123",   # plain for now (local demo)
    "roles": ["admin"],
}

def verify_password(plain: str) -> bool:
    return plain == DEMO_USER["password"]

def create_access_token(sub: str, roles: list[str]) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.JWT_EXPIRES_MINUTES)
    payload = {
        "iss": settings.JWT_ISSUER,
        "sub": sub,
        "roles": roles,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"], issuer=settings.JWT_ISSUER)
    except JWTError as e:
        raise ValueError(str(e)) from e
