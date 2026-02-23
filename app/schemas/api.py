from math import ceil
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationInfo(BaseModel):
    page: int
    limit: int
    total_pages: int
    total_items: int
    has_next: bool
    has_prev: bool

    @classmethod
    def build(cls, page: int, limit: int, total_items: int) -> "PaginationInfo":
        total_pages = max(1, ceil(total_items / limit))
        return cls(
            page=page,
            limit=limit,
            total_pages=total_pages,
            total_items=total_items,
            has_next=page < total_pages,
            has_prev=page > 1,
        )


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: T
    metadata: Optional[dict[str, Any]] = None


class PaginatedApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: list[T]
    pagination: PaginationInfo
    metadata: Optional[dict[str, Any]] = None
