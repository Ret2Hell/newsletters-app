from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel):
    message: str


class SuccessResponse(BaseResponse, Generic[T]):
    data: T


class ErrorResponse(BaseResponse):
    pass
