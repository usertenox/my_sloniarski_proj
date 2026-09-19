from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dependencies import get_principal, get_project_service
from src.authorization.principal import Principal
from src.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from src.services.project_service import ProjectService


project_router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@project_router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project_data: ProjectCreate,
    principal: Annotated[Principal, Depends(get_principal)],
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectResponse:
    return await service.create(
        user_id=principal.user_id,
        project_data=project_data,
    )


@project_router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def get_project(
    project_id: UUID,
    principal: Annotated[Principal, Depends(get_principal)],
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectResponse:
    return await service.get_project(
        project_id=project_id,
        user_id=principal.user_id,
    )


@project_router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    principal: Annotated[Principal, Depends(get_principal)],
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectResponse:
    return await service.update(
        project_id=project_id,
        user_id=principal.user_id,
        update_data=project_data,
    )


@project_router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: UUID,
    principal: Annotated[Principal, Depends(get_principal)],
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> None:
    await service.delete(
        project_id=project_id,
        user_id=principal.user_id,
    )
