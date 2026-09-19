# RBAC:
# manager → documents.read

# Permission - что надо сделать

# policies - при каких условиях на конкретных строках в бд(Row-Level Security (RLS), ограничение доступа к данным на уровне строк)

# ReBAC:
# manager belongs to project X (реализуется с помощью owner тут)

# PBAC (Policy-Based Access Control) - authorize(), оюъединяет ReBAC и RBAC


from enum import StrEnum
from dataclasses import dataclass

from src.core.enums import ProjectRole


class ProjectPermission(StrEnum):
    READ = "read"
    DELETE = "delete"
    UPDATE = "update"

    ADD_MEMBER = "add_member"
    UPDATE_MEMBER = "update_member"
    REMOVE_MEMBER = "remove_member"  


@dataclass(frozen=True) # security decision input
class ProjectAuthContext:
    is_owner: bool
    role: ProjectRole | None = None


class ProjectPolicy:

    @staticmethod
    def authorize(action: ProjectPermission, context: ProjectAuthContext) -> bool:

        if context.is_owner:
            return True         

        if action == ProjectPermission.READ:
            return context.role in {
                ProjectRole.ADMIN,
                ProjectRole.EDITOR,
                ProjectRole.VIEWER,
            }
        
        if action == ProjectPermission.UPDATE:
            return context.role == ProjectRole.ADMIN

        if action == ProjectPermission.DELETE:
            return False

        return False

    

        

        

