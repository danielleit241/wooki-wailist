from datetime import datetime, timezone
from enum import StrEnum
import uuid

from sqlalchemy import UUID, Boolean, Column, DateTime, String

from .database import Base

class UserStatus(StrEnum):
    PENDING = "pending"
    INVITED = "invited"

class User(Base):
    __tablename__ = "waiting_list_users"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        index=True
    )  

    email = Column(String(255), unique=True, nullable=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=True, index=True)    
    full_name = Column(String(100), nullable=True)
    
    referral_code = Column(String(20), nullable=True, index=True)
    status = Column(String(20), default=UserStatus.PENDING.value)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User(email={self.email}, status={self.status})>"