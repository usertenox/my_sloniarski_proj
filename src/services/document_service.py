from uuid import UUID

from src.models.document import Document
from src.repositories.document_repo import DocumentRepository
from src.repositories.project_member_repo import ProjectMemberRepo
from src.repositories.project_repo import ProjectRepository
from src.policies.project_policy import ProjectAuthContext
from src.utils.errors import ProjectNotFound, AccessDenied

class DocumentService:

    def __init__(
            self, 
            doc_repo: DocumentRepository,
            proj_repo: ProjectRepository,
            proj_member_repo: ProjectMemberRepo,
        ):
        self.doc_repo = doc_repo
        self.proj_repo = proj_repo
        self.proj_member_repo = proj_member_repo

        async def _get_auth_context(
                proj_id: UUID,
                user_id: UUID,
            ) -> ProjectAuthContext:

            project = await self.proj_repo.get_by_id(proj_id=proj_id)

            if project is None:
                raise ProjectNotFound
            
            if project.owner_id == user_id:
                return ProjectAuthContext(is_owner=True)
            
            proj_member = await self.proj_member_repo.get_by_project_and_user(
                project_id=proj_id, 
                user_id=user_id
            )

            if proj_member is None:
                raise AccessDenied

            return ProjectAuthContext(
                is_owner=False,
                role=proj_member.role,
            )

    async def create_document(
            self, 
            project_id: UUID, 
            created_by_id: UUID,
            title: str,
            content: str
        ) -> Document:

        document = self.doc_repo.create(
            project_id=project_id,
            created_by_id=created_by_id,
            title=title,
            content=content,
        )