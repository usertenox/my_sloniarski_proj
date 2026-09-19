from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.project_member import ProjectMember
from src.core.enums import ProjectRole


class ProjectMemberRepo:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
            self, 
            project_id: UUID, 
            user_id: UUID, 
            role: ProjectRole
            ) -> ProjectMember:

        project_member = ProjectMember(
            project_id=project_id,
            user_id=user_id,
            role=role,
        )

        self.db.add(project_member)
        await self.db.flush()
        await self.db.refresh(project_member)
        
        return project_member

    async def get_by_project_and_user(
        self,
        project_id: UUID,
        user_id: UUID,
    ) -> ProjectMember | None:

        stmt = select(ProjectMember).where(
            ProjectMember.project_id==project_id,
            ProjectMember.user_id==user_id,
            )
        
        res = await self.db.execute(stmt)

        return res.scalar_one_or_none()

    async def get_by_project_id(
        self,
        project_id: UUID,
    ) -> list[ProjectMember]:

        stmt = select(ProjectMember).where(
            ProjectMember.project_id == project_id
        )

        result = await self.db.execute(stmt)

        return result.scalars().all() # берет все об.собирает в список


    async def update_role(
        self,
        project_member: ProjectMember,
        role: ProjectRole,
    ) -> ProjectMember:

        project_member.role = role

        await self.db.flush()

        return project_member

    async def delete(
        self,
        project_member: ProjectMember,
    ) -> None:
        
        await self.db.delete(project_member)
        await self.db.flush()