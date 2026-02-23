from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import User, UserStatus
from app.schemas import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_users(self) -> list[User]:
        return self.db.query(User).all()

    def create_user(self, payload: UserCreate) -> User:
        user = User(
            email=payload.email,
            phone_number=payload.phone_number,
            full_name=payload.full_name,
            referral_code=payload.referral_code,
            status=UserStatus.PENDING.value,
            is_active=True,
        )
        self.db.add(user)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise
        self.db.refresh(user)
        return user
