from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, model_validator


class UserCreate(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    full_name: Optional[str] = None
    referral_code: Optional[str] = None

    @field_validator("phone_number", "full_name", "referral_code", mode="before")
    @classmethod
    def normalize_optional_text(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned or None
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        allowed_chars = set("+0123456789")
        if any(char not in allowed_chars for char in value):
            raise ValueError("phone_number chỉ được chứa số và ký tự '+'")

        digits_count = sum(char.isdigit() for char in value)
        if digits_count < 9 or digits_count > 15:
            raise ValueError("phone_number phải có từ 9 đến 15 chữ số")

        return value

    @model_validator(mode="after")
    def validate_contact_info(self):
        if not self.email and not self.phone_number:
            raise ValueError("Cần cung cấp ít nhất email hoặc phone_number")
        return self


class UserResponse(BaseModel):
    id: UUID
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    full_name: Optional[str] = None
    referral_code: Optional[str] = None
    status: str
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
