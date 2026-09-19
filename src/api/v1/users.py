from fastapi import APIRouter, Depends
from typing import Annotated

from src.schemas.auth import UserResponse
from src.models.user import User
from src.api.dependencies import get_current_user


api_user = APIRouter(prefix="/users", tags=["Users"])


@api_user.get("/me", response_model=UserResponse)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    return UserResponse.model_validate(current_user)
