from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.config import settings


api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def verify_api_key(api_key: str | None = Security(api_key_header)) -> str:
    if not api_key or api_key != settings.X_API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return api_key