from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse


api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def verify_api_key(api_key: str | None = Security(api_key_header)) -> str:
    if not api_key or api_key != settings.X_API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return api_key

router = APIRouter(
    prefix=settings.API_PREFIX + "/users",
    tags=["Users"],
)

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@router.get("", response_model=list[UserResponse], dependencies=[Depends(verify_api_key)])
def get_users(service: UserService = Depends(get_user_service)):
    return service.list_users()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(payload)
