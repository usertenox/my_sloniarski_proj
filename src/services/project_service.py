from uuid import UUID

from src.models.project import Project
from src.schemas.project import ProjectCreate, ProjectUpdate
from src.repositories.project_repo import ProjectRepository
from src.repositories.project_member_repo import ProjectMemberRepo
from src.utils.errors import ProjectNotFound, AccessDenied
from src.policies.project_policy import (
    ProjectPolicy,
    ProjectPermission,
    ProjectAuthContext,
)


class ProjectService:

    def __init__(self, project_repo: ProjectRepository, project_member_repo: ProjectMemberRepo):
        self.project_repo = project_repo
        self.project_member_repo = project_member_repo

    async def _get_auth_context(self, user_id: UUID, project: Project) -> ProjectAuthContext:
        if project.owner_id == user_id:
            return ProjectAuthContext(is_owner=True)

        project_member = await self.project_member_repo.get_by_project_and_user(
            project_id=project.id,
            user_id=user_id,
        )

        return ProjectAuthContext(
            is_owner=False,
            role=project_member.role if project_member else None,
        )

    async def create(self, user_id: UUID, project_data: ProjectCreate) -> Project:
        owner_id = user_id
        project = await self.project_repo.create(name=project_data.name, owner_id=owner_id)
        return project

    async def get_project(self, project_id: UUID, user_id: UUID) -> Project:
        project = await self.project_repo.get_by_id(project_id)

        if project is None:
            raise ProjectNotFound()

        context = await self._get_auth_context(user_id, project=project)

        allowed = ProjectPolicy.authorize(
            action=ProjectPermission.READ,
            context=context,
        )

        if not allowed:
            raise AccessDenied()

        return project

    async def update(self, project_id: UUID, user_id: UUID, update_data: ProjectUpdate) -> Project:
        project = await self.project_repo.get_by_id(project_id=project_id)

        if project is None:
            raise ProjectNotFound()

        context = await self._get_auth_context(user_id=user_id, project=project)

        allowed = ProjectPolicy.authorize(
            action=ProjectPermission.UPDATE,
            context=context,
        )

        if not allowed:
            raise AccessDenied()

        return await self.project_repo.update(project=project, project_data=update_data)

    async def delete(self, project_id: UUID, user_id: UUID) -> None:
        project = await self.project_repo.get_by_id(project_id=project_id)

        if project is None:
            raise ProjectNotFound()

        allowed = ProjectPolicy.authorize(
            action=ProjectPermission.DELETE,
            context=await self._get_auth_context(user_id=user_id, project=project),
        )

        if allowed:
            return await self.project_repo.delete(project=project)

        raise AccessDenied()
