from dataclasses import dataclass
from uuid import UUID

from src.core.enums import ProjectRole


@dataclass(frozen=True)
class ProjectAccessContext:
    """Describes a user's relationship to a project"""

    user_id: UUID
    project_id: UUID
    is_owner: bool
    role: ProjectRole | None = None