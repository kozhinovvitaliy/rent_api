from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class GetUserResponse(BaseModel):
    first_name: str
    last_name: str
    login: str
    sex: str


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    sex: Literal["MALE", "FEMALE"]
    login: str
    password: str


class UserLoginRequest(BaseModel):
    login: str
    password: str


class UserLoginResponse(BaseModel):
    authentication_code: UUID
