from uuid import UUID

from src.core.access.context import ProjectAccessContext
from src.models.project import Project
from src.repositories.project_member_repo import ProjectMemberRepo


class ProjectAccessResolver:
    """Resolves a users relationship to a project"""

    def __init__(self, project_member_repo: ProjectMemberRepo):
        self.project_member_repo = project_member_repo

    async def resolve(
        self,
        project: Project,
        user_id: UUID,
    ) -> ProjectAccessContext:
        if project.owner_id == user_id:
            return ProjectAccessContext(
                user_id=user_id,
                project_id=project.id,
                is_owner=True,
            )

        member = await self.project_member_repo.get_by_project_and_user(
            project_id=project.id,
            user_id=user_id,
        )

        return ProjectAccessContext(
            user_id=user_id,
            project_id=project.id,
            is_owner=False,
            role=member.role if member is not None else None,
        )
