from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

Username = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=3, max_length=50),
]

Password = Annotated[
    str,
    StringConstraints(min_length=12, max_length=128),
]


class RegisterRequest(BaseModel):
    username: Username
    email: EmailStr
    password: Password


class LoginRequest(BaseModel):
    email: EmailStr
    password: Password


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) # срабатывает при model_validate

    id: UUID
    username: str
    email: EmailStr


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"