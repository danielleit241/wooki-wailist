from fastapi import APIRouter, Depends, HTTPException, Query, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.schemas.api import PaginationInfo
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserListApiResponse, UserSingleApiResponse, UserResponse


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

@router.get("", response_model=UserListApiResponse, dependencies=[Depends(verify_api_key)])
def get_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    service: UserService = Depends(get_user_service),
):
    users, total_items = service.list_users(page=page, limit=limit)
    return UserListApiResponse(
        success=True,
        message="Lấy dữ liệu thành công",
        data=[UserResponse.model_validate(user) for user in users],
        pagination=PaginationInfo.build(page=page, limit=limit, total_items=total_items),
        metadata=None,
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserSingleApiResponse)
def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    user = service.create_user(payload)
    return UserSingleApiResponse(
        success=True,
        message="Tạo user thành công",
        data=UserResponse.model_validate(user),
        metadata=None,
    )
