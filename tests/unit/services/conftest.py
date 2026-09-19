import pytest_asyncio

from unittest.mock import AsyncMock

from src.services.project_member_service import ProjectMemberService


@pytest_asyncio.fixture
def project_repo():
    return AsyncMock()


@pytest_asyncio.fixture
def project_member_repo():
    return AsyncMock()


@pytest_asyncio.fixture
def user_repo():
    return AsyncMock()


@pytest_asyncio.fixture
def project_member_service(
    project_repo,
    project_member_repo,
    user_repo,
):
    return ProjectMemberService(
        project_repo=project_repo,
        project_member_repo=project_member_repo,
        user_repo=user_repo,
    )