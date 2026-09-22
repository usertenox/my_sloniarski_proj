from dataclasses import dataclass
from uuid import UUID
from collections.abc import Mapping

from src.core.enums import ProjectRole
from src.core.access.permissions import Permissions
from src.core.access.policies import Policies


@dataclass(frozen=True, slots=True)
class AccessContext:
    """Describes a users relationship to a project"""

    user_id: UUID
    project_id: UUID
    is_owner: bool
    permission: Permissions # чтобы выбрать, для чего взять policies
    granted_permissions: frozenset[Permissions]
    policies: Mapping[Permissions, tuple[Policies, ...]]
    role: ProjectRole | None = None