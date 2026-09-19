from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dependencies import get_principal, get_project_member_service
from src.authorization.principal import Principal
from src.schemas.project_member import MemberCreate, MemberResponse, MemberRoleUpdate
from src.services.project_member_service import ProjectMemberService


project_member_router = APIRouter(
    prefix="/projects/{project_id}/members",
    tags=["Project Members"],
)


@project_member_router.post(
    "",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_member(
    project_id: UUID,
    member_data: MemberCreate,
    principal: Annotated[Principal, Depends(get_principal)],
    service: Annotated[ProjectMemberService, Depends(get_project_member_service)],
) -> MemberResponse:
    return await service.add_member(
        project_id=project_id,
        user_id=principal.user_id,
        new_member_data=member_data,
    )


@project_member_router.get(
    "",
    response_model=list[MemberResponse],
)
async def list_members(
    project_id: UUID,
    principal: Annotated[Principal, Depends(get_principal)],
    service: Annotated[ProjectMemberService, Depends(get_project_member_service)],
) -> list[MemberResponse]:
    return await service.list_members(
        project_id=project_id,
        user_id=principal.user_id,
    )


@project_member_router.patch(
    "/{target_user_id}",
    response_model=MemberResponse,
)
async def update_member_role(
    project_id: UUID,
    target_user_id: UUID,
    role_data: MemberRoleUpdate,
    principal: Annotated[Principal, Depends(get_principal)],
    service: Annotated[ProjectMemberService, Depends(get_project_member_service)],
) -> MemberResponse:
    return await service.update_role(
        project_id=project_id,
        user_id=principal.user_id,
        new_role=role_data,
        target_user_id=target_user_id,
    )


@project_member_router.delete(
    "/{target_user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_member(
    project_id: UUID,
    target_user_id: UUID,
    principal: Annotated[Principal, Depends(get_principal)],
    service: Annotated[ProjectMemberService, Depends(get_project_member_service)],
) -> None:
    await service.remove_member(
        project_id=project_id,
        user_id=principal.user_id,
        target_user_id=target_user_id,
    )
