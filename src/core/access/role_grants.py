from dataclasses import dataclass
from collections.abc import Mapping

from src.core.access.permissions import Permissions
from src.core.enums import ProjectRole
from src.core.access.policies import Policies


@dataclass(frozen=True, slots=True)
class RoleGrant:
    """Grants possibilities (permissions) 
    of role and current policies"""

    permissions: frozenset[Permissions] # обязательно, так как мб без политик
    policies: Mapping[Permissions, tuple[Policies, ...]]
# Mapping юзаем, потому что это хорошее правило 
# типизации, может захавать объект, в котором поиск по ключу
# ... - любое количесво объектов типа Permissions

# какие permissions есть у роли
# какие policies привязаны к текущему permission



OWNER_GRANT = RoleGrant(
        permissions=frozenset(Permissions),
        policies={}
    )


ROLE_GRANTS = {
    ProjectRole.ADMIN: RoleGrant(
        permissions=frozenset( # пихаем объект-список и set его итерирует
            [
                Permissions.PROJECT_READ,
                Permissions.PROJECT_UPDATE,

                Permissions.MEMBER_ADD,
                Permissions.MEMBER_READ,
                Permissions.MEMBER_REMOVE,
                Permissions.MEMBER_UPDATE_ROLE,

                Permissions.DOCUMENT_CREATE,
                Permissions.DOCUMENT_DELETE,
                Permissions.DOCUMENT_READ,
                Permissions.DOCUMENT_UPDATE,
            ]
        ),

        policies={}
    ),  

    ProjectRole.EDITOR: RoleGrant(
        permissions=frozenset(
            [
                Permissions.PROJECT_READ,

                Permissions.MEMBER_READ,

                Permissions.DOCUMENT_CREATE,
                Permissions.DOCUMENT_READ,
                Permissions.DOCUMENT_UPDATE,
            ]
        ),

        policies={
            Permissions.DOCUMENT_READ: (
                Policies.NOT_DELETED,
            ),
            Permissions.DOCUMENT_UPDATE: (
                Policies.NOT_DELETED,
            ),
        }
    ),

    ProjectRole.VIEWER: RoleGrant(
        permissions=frozenset(
            [
                Permissions.PROJECT_READ,

                Permissions.MEMBER_READ,

                Permissions.DOCUMENT_READ,
            ]
        ),

        policies={
            Permissions.DOCUMENT_READ: (
                Policies.NOT_DELETED,
            ),
        }
    ),
}


# def get_role_grant(context: AccessContext) -> RoleGrant:
#     if context.is_owner:
#         return OWNER_GRANT

#     if context.role is None:
#         raise AccessDenied()

#     return ROLE_GRANTS[context.role]