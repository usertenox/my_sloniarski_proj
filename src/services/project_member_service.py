from uuid import UUID

from src.repositories.project_member_repo import ProjectMemberRepo
from src.repositories.project_repo import ProjectRepository
from src.repositories.user_repo import UserRepository
from src.schemas.project_member import MemberCreate, MemberRoleUpdate
from src.models.project_member import ProjectMember
from src.models.project import Project
from src.utils.errors import (
    ProjectNotFound,
    AccessDenied,
    UserAlreadyExists,
    InvalidProjectMemberTarget,
    UserNotFound,
    MemberNotFound,
)
from src.policies.project_member_policy import (
    ProjectAuthContext,
    ProjectMemberPolicy,
    ProjectMemberPermission,
)


class ProjectMemberService:

    def __init__(
        self,
        project_member_repo: ProjectMemberRepo,
        project_repo: ProjectRepository,
        user_repo: UserRepository,
    ):
        self.project_member_repo = project_member_repo
        self.project_repo = project_repo
        self.user_repo = user_repo

    async def _get_auth_context(
        self,
        project: Project,
        user_id: UUID,
    ) -> ProjectAuthContext:
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

    async def add_member(
        self,
        project_id: UUID,
        user_id: UUID,
        new_member_data: MemberCreate,
    ) -> ProjectMember:
        project = await self.project_repo.get_by_id(project_id=project_id)

        if project is None:
            raise ProjectNotFound()

        context = await self._get_auth_context(
            project=project,
            user_id=user_id,
        )

        allowed = ProjectMemberPolicy.authorize(
            context=context,
            action=ProjectMemberPermission.ADD,
        )

        can_assign_role = ProjectMemberPolicy.can_assign_role(
            context=context,
            new_role=new_member_data.role,
        )

        if not allowed or not can_assign_role:
            raise AccessDenied()

        if new_member_data.user_id == project.owner_id:
            raise InvalidProjectMemberTarget()

        existing_member = await self.project_member_repo.get_by_project_and_user(
            project_id=project.id,
            user_id=new_member_data.user_id,
        )

        if existing_member is not None:
            raise UserAlreadyExists()

        user = await self.user_repo.get_by_id(new_member_data.user_id)

        if user is None:
            raise UserNotFound()

        return await self.project_member_repo.create(
            project_id=project.id,
            user_id=new_member_data.user_id,
            role=new_member_data.role,
        )

    async def update_role(
        self,
        project_id: UUID,
        user_id: UUID,
        new_role: MemberRoleUpdate,
        target_user_id: UUID,
    ) -> ProjectMember:
        project = await self.project_repo.get_by_id(project_id=project_id)

        if project is None:
            raise ProjectNotFound()

        context = await self._get_auth_context(
            project=project,
            user_id=user_id,
        )

        allowed = ProjectMemberPolicy.authorize(
            context=context,
            action=ProjectMemberPermission.UPDATE_ROLE,
        )

        if not allowed:
            raise AccessDenied()

        target_member = await self.project_member_repo.get_by_project_and_user(
            project_id=project.id,
            user_id=target_user_id,
        )

        if target_member is None:
            raise MemberNotFound()

        can_change_role = ProjectMemberPolicy.can_change_role(
            context=context,
            new_role=new_role.role,
            target_role=target_member.role,
        )

        if not can_change_role:
            raise AccessDenied()

        return await self.project_member_repo.update_role(
            project_member=target_member,
            role=new_role.role,
        )

    async def remove_member(
        self,
        project_id: UUID,
        user_id: UUID,
        target_user_id: UUID,
    ) -> None:
        project = await self.project_repo.get_by_id(project_id=project_id)

        if project is None:
            raise ProjectNotFound()

        context = await self._get_auth_context(
            project=project,
            user_id=user_id,
        )

        allowed = ProjectMemberPolicy.authorize(
            context=context,
            action=ProjectMemberPermission.REMOVE,
        )

        if not allowed:
            raise AccessDenied()

        target_member = await self.project_member_repo.get_by_project_and_user(
            project_id=project_id,
            user_id=target_user_id,
        )

        if target_member is None:
            raise MemberNotFound()

        can_remove = ProjectMemberPolicy.can_remove_member(
            context=context,
            target_role=target_member.role,
            is_self=target_member.user_id == user_id,
        )

        if not can_remove:
            raise AccessDenied()

        await self.project_member_repo.delete(project_member=target_member)

    async def list_members(
        self,
        project_id: UUID,
        user_id: UUID,
    ) -> list[ProjectMember]:
        project = await self.project_repo.get_by_id(project_id=project_id)

        if project is None:
            raise ProjectNotFound()

        context = await self._get_auth_context(
            project=project,
            user_id=user_id,
        )

        allowed = ProjectMemberPolicy.authorize(
            context=context,
            action=ProjectMemberPermission.READ,
        )

        if not allowed:
            raise AccessDenied()

        return await self.project_member_repo.get_by_project_id(project_id=project_id)
