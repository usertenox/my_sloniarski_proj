from src.core.access.permissions import Permission
from src.core.enums import ProjectRole


ROLE_PERMISSIONS: dict[ProjectRole, set[Permission]] = {
    ProjectRole.ADMIN: {
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.MEMBER_READ,
        Permission.MEMBER_ADD,
        Permission.MEMBER_UPDATE_ROLE,
        Permission.MEMBER_REMOVE,
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_READ,
        Permission.DOCUMENT_UPDATE,
        Permission.DOCUMENT_DELETE,
    },
    ProjectRole.EDITOR: {
        Permission.PROJECT_READ,
        Permission.MEMBER_READ,
        Permission.DOCUMENT_CREATE,
        Permission.DOCUMENT_READ,
        Permission.DOCUMENT_UPDATE,
    },
    ProjectRole.VIEWER: {
        Permission.PROJECT_READ,
        Permission.MEMBER_READ,
        Permission.DOCUMENT_READ,
    },
}
