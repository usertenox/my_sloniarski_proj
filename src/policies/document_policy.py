from enum import StrEnum

from src.policies.project_policy import ProjectAuthContext
from src.core.enums import ProjectRole


class DocumentPermission(StrEnum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class DocumentPolicy:

    _PERMISSIONS = {
        ProjectRole.ADMIN: {
            DocumentPermission.CREATE,
            DocumentPermission.READ,
            DocumentPermission.UPDATE,
            DocumentPermission.DELETE,
        },
        ProjectRole.EDITOR: {
            DocumentPermission.CREATE,
            DocumentPermission.READ,
            DocumentPermission.UPDATE,
        },
        ProjectRole.VIEWER: {
            DocumentPermission.READ,
        },
    }

    @classmethod
    def authorize(
        cls,
        context: ProjectAuthContext,
        action: DocumentPermission,
    ) -> bool:

        if context.is_owner:
            return True

        return action in cls._PERMISSIONS.get(context.role, ()) # гетим по роли, если нету, то проверку в пустом кортеже
        # и будет False
    
