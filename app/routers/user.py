from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.middleware import verify_api_key
from app.schemas.api import PaginationInfo
from app.schemas.user import UserCreate, UserListApiResponse, UserSingleApiResponse, UserResponse
from app.services.user_service import UserService

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
