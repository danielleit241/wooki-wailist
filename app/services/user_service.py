from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def list_users(self):
        return self.repository.list_users()

    def create_user(self, payload: UserCreate):
        try:
            return self.repository.create_user(payload)
        except IntegrityError as exc:
            error_text = str(exc.orig)

            if "ix_waiting_list_users_email" in error_text:
                detail = "Email đã tồn tại"
            elif "ix_waiting_list_users_phone_number" in error_text:
                detail = "Số điện thoại đã tồn tại"
            else:
                detail = "Dữ liệu bị trùng với bản ghi đã tồn tại"

            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail) from exc