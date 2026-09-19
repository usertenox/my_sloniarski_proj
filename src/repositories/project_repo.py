from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.models.project import Project
from src.schemas.project import ProjectUpdate


class ProjectRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, name: str, owner_id: UUID) -> Project:
        project = Project(
            name=name,
            owner_id=owner_id,
        )

        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)

        return project


    async def get_by_id(self, project_id: UUID) -> Project | None:

        query = select(Project).where(Project.id==project_id)

        res = await self.db.execute(query)

        return res.scalar_one_or_none()


    async def update(
            self, 
            project: Project, 
            project_data: ProjectUpdate
            ) -> Project:

        updates = project_data.model_dump(exclude_unset=True) # превращает Pydantic-модель в словарь:

        for field, value in updates.items():
            setattr(project, field, value) # project.name = project_data.name
            
        await self.db.flush()

        return project

    async def delete(self, project: Project) -> None:

        self.db.delete(project)

        await self.db.flush()
