from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import decode_access_token
from src.db.context import get_db
from src.models.user import User
from src.repositories.project_member_repo import ProjectMemberRepo
from src.repositories.project_repo import ProjectRepository
from src.repositories.refresh_repo import RefreshTokenRepo
from src.repositories.user_repo import UserRepository
from src.repositories.document_repo import DocumentRepository
from src.services.auth_service import AuthService
from src.services.project_member_service import ProjectMemberService
from src.services.project_service import ProjectService
from src.services.document_service import DocumentService
from src.utils.errors import InvalidJWT
from src.authorization.principal import Principal


bearer_scheme = HTTPBearer(auto_error=False)


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_ref_token_repo(db: AsyncSession = Depends(get_db)) -> RefreshTokenRepo:
    return RefreshTokenRepo(db)


def get_project_repo(db: AsyncSession = Depends(get_db)) -> ProjectRepository:
    return ProjectRepository(db)


def get_project_member_repo(db: AsyncSession = Depends(get_db)) -> ProjectMemberRepo:
    return ProjectMemberRepo(db)

def get_document_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> DocumentRepository:
    return DocumentRepository(db)


def get_auth_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
    ref_token_repo: Annotated[RefreshTokenRepo, Depends(get_ref_token_repo)],
) -> AuthService:
    return AuthService(
        user_repo=user_repo,
        ref_token_repo=ref_token_repo,
    )


def get_project_service(
    project_repo: Annotated[ProjectRepository, Depends(get_project_repo)],
    project_member_repo: Annotated[
        ProjectMemberRepo,
        Depends(get_project_member_repo),
    ],
) -> ProjectService:
    return ProjectService(
        project_repo=project_repo,
        project_member_repo=project_member_repo,
    )


def get_project_member_service(
    project_repo: Annotated[ProjectRepository, Depends(get_project_repo)],
    project_member_repo: Annotated[
        ProjectMemberRepo,
        Depends(get_project_member_repo),
    ],
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> ProjectMemberService:
    return ProjectMemberService(
        project_member_repo=project_member_repo,
        project_repo=project_repo,
        user_repo=user_repo,
    )


def get_document_service(
        doc_repo: Annotated[
            DocumentRepository, Depends(get_document_repo)
            ]
        ) -> DocumentService:
    return DocumentService(doc_repo=doc_repo)


async def get_principal(
        credentials: Annotated[
            HTTPAuthorizationCredentials | None, 
            Depends(bearer_scheme)
        ]
    ) -> Principal:

    if credentials is None:
        raise InvalidJWT()

    token = credentials.credentials.strip()

    if not token:
        raise InvalidJWT()

    user_id = decode_access_token(token=token)

    return Principal(user_id=user_id)

#     HTTPAuthorizationCredentials(
#     scheme="Bearer", 
#     credentials="my_secret_token_123"
# )

async def get_current_user(
    principal: Annotated[Principal, Depends(get_principal)],
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> User:
    user = await user_repo.get_by_id(principal.user_id)

    if user is None:
        raise InvalidJWT()

    return user
