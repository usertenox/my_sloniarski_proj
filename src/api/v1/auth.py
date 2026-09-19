from fastapi import APIRouter, Depends, Response, status
from typing import Annotated

from src.schemas.auth import (
    AuthResponse,
    RegisterRequest,
    LoginRequest,
    TokenPairResponse,
    RefreshRequest,
)
from src.api.dependencies import get_auth_service, get_principal
from src.services.auth_service import AuthService
from src.authorization.principal import Principal


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", response_model=AuthResponse, status_code=201)
async def register(
    request: RegisterRequest,
    services: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    return await services.register(request=request)


@auth_router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    return await service.login(request=request)


@auth_router.post("/refresh", response_model=TokenPairResponse)
async def refresh(
    request: RefreshRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenPairResponse:
    return await service.refresh(request.refresh_token)


@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: RefreshRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> Response:
    await service.logout(request.refresh_token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@auth_router.post("/logout_all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    principal: Annotated[Principal, Depends(get_principal)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> Response:
    await service.logout_all(principal.user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
