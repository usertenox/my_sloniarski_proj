import pytest

from src.core.enums import ProjectRole
from src.policies.project_member_policy import (
    ProjectMemberPermission,
    ProjectMemberPolicy,
)
from src.policies.project_policy import ProjectAuthContext


@pytest.mark.parametrize(
    "context,action,expected",
    [
        # OWNER
        (
            ProjectAuthContext(is_owner=True),
            ProjectMemberPermission.READ,
            True,
        ),
        (
            ProjectAuthContext(is_owner=True),
            ProjectMemberPermission.ADD,
            True,
        ),

        # ADMIN
        (
            ProjectAuthContext(is_owner=False, role=ProjectRole.ADMIN),
            ProjectMemberPermission.READ,
            True,
        ),
        (
            ProjectAuthContext(is_owner=False, role=ProjectRole.ADMIN),
            ProjectMemberPermission.REMOVE,
            True,
        ),

        # EDITOR
        (
            ProjectAuthContext(is_owner=False, role=ProjectRole.EDITOR),
            ProjectMemberPermission.READ,
            True,
        ),
        (
            ProjectAuthContext(is_owner=False, role=ProjectRole.EDITOR),
            ProjectMemberPermission.ADD,
            False,
        ),

        # VIEWER
        (
            ProjectAuthContext(is_owner=False, role=ProjectRole.VIEWER),
            ProjectMemberPermission.READ,
            True,
        ),
        (
            ProjectAuthContext(is_owner=False, role=ProjectRole.VIEWER),
            ProjectMemberPermission.UPDATE_ROLE,
            False,
        ),

        # OUTSIDER
        (
            ProjectAuthContext(is_owner=False, role=None),
            ProjectMemberPermission.READ,
            False,
        ),
        (
            ProjectAuthContext(is_owner=False, role=None),
            ProjectMemberPermission.ADD,
            False,
        ),
    ],
)
def test_authorize(context, action, expected):
    assert ProjectMemberPolicy.authorize(context, action) is expected