from fastapi import APIRouter

from src.api.v1.auth import auth_router
from src.api.v1.users import api_user
from src.api.v1.projects import project_router
from src.api.v1.project_members import project_member_router


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(api_user)
api_router.include_router(project_router)
api_router.include_router(project_member_router)
