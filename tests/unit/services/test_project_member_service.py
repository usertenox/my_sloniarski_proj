import pytest

from uuid import uuid4

from src.models.project import Project
from src.models.project_member import ProjectMember
from src.core.enums import ProjectRole
from src.models.user import User
from src.schemas.project_member import MemberCreate
from src.utils.errors import ProjectNotFound, AccessDenied


@pytest.mark.asyncio
async def test_add_member_project_not_found(
    project_member_service,
):
    project_id = uuid4()

    current_user = User(
        id=uuid4(),
        username="owner",
        email="owner@example.com",
        password_hash="hash",
    )

    new_member = MemberCreate(
        user_id=uuid4(),
        role=ProjectRole.VIEWER,
    )

    project_member_service.project_repo.get_by_id.return_value = None

    with pytest.raises(ProjectNotFound):
        await project_member_service.add_member(
            project_id=project_id,
            user_id=current_user.id,
            new_member_data=new_member,
        )


@pytest.mark.asyncio
async def test_add_member_access_denied(project_member_service):

    project_id = uuid4()
    owner_id = uuid4()

    project = Project(
        id=project_id,
        owner_id=owner_id,
        name="Test project",
    )

    current_user = User(
        id=uuid4(),
        username="owner",
        email="owner@example.com",
        password_hash="hash",
    )

    current_member = ProjectMember(
        project_id=project_id,
        user_id=current_user.id,
        role=ProjectRole.VIEWER,
    )

    new_member = MemberCreate(
        user_id=uuid4(),
        role=ProjectRole.VIEWER,
    )

    project_member_service.project_repo.get_by_id.return_value = project
    project_member_service.project_member_repo.get_by_project_and_user.return_value = current_member

    with pytest.raises(AccessDenied):
        await project_member_service.add_member(
            project_id=project.id,
            user_id=current_user.id,
            new_member_data=new_member,
        )