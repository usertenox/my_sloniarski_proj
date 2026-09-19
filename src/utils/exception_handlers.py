from fastapi import status, Request, FastAPI
from fastapi.responses import JSONResponse

from src.utils.errors import (
    UserAlreadyExists, 
    InvalidCredentials, 
    AppError, 
    InvalidJWT,
    ProjectNotFound,
    AccessDenied,
    MemberExists,
    InvalidProjectMemberTarget,
    UserNotFound,
    MemberNotFound,
)


ERROR_STATUS_MAP = {
    UserAlreadyExists: status.HTTP_409_CONFLICT,
    InvalidCredentials: status.HTTP_401_UNAUTHORIZED,
    InvalidJWT: status.HTTP_401_UNAUTHORIZED,
    ProjectNotFound: status.HTTP_404_NOT_FOUND,
    AccessDenied: status.HTTP_403_FORBIDDEN,
    MemberExists: status.HTTP_409_CONFLICT,
    InvalidProjectMemberTarget: status.HTTP_409_CONFLICT,
    UserNotFound: status.HTTP_404_NOT_FOUND,
    MemberNotFound: status.HTTP_404_NOT_FOUND,
}


def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=ERROR_STATUS_MAP.get(type(exc), status.HTTP_400_BAD_REQUEST), # так это <class '__main__.InvalidJWT'>, py это видит как InvalidJWT
        content={"detail": str(exc)}
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)