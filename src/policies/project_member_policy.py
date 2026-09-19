from enum import StrEnum

from src.policies.project_policy import ProjectAuthContext
from src.core.enums import ProjectRole


class ProjectMemberPermission(StrEnum):
    ADD = "add_member"
    UPDATE_ROLE = "update_member_role"
    REMOVE = "remove_member"
    READ = "read"


class ProjectMemberPolicy:

    @staticmethod
    def authorize(
        context: ProjectAuthContext, 
        action: ProjectMemberPermission,
    ) -> bool:

        if context.is_owner:
            return True

        if action is ProjectMemberPermission.READ:
            return context.role in{
                ProjectRole.ADMIN,
                ProjectRole.EDITOR,
                ProjectRole.VIEWER,
            }

        if action in {
            ProjectMemberPermission.ADD,
            ProjectMemberPermission.UPDATE_ROLE,
            ProjectMemberPermission.REMOVE,
            }:

            return context.role is ProjectRole.ADMIN

        return False

    @staticmethod
    def can_assign_role(
        context: ProjectAuthContext, 
        new_role: ProjectRole
        ) -> bool:

        if context.is_owner:
            return True

        if context.role is ProjectRole.ADMIN:
            return new_role in{
                ProjectRole.EDITOR,
                ProjectRole.VIEWER,
            }

        return False


    @staticmethod
    def can_change_role(
        context: ProjectAuthContext, 
        new_role: ProjectRole,
        target_role: ProjectRole,
    ) -> bool:

        if context.is_owner:
            return True

        if context.role == ProjectRole.ADMIN and target_role is not ProjectRole.ADMIN:
            return new_role in {
                ProjectRole.VIEWER,
                ProjectRole.EDITOR,
            }

        return False

    @staticmethod
    def can_remove_member(
        context: ProjectAuthContext, 
        target_role: ProjectRole,
        is_self: bool,
    ) -> bool:

        if context.is_owner:
             return True

        if context.role == ProjectRole.ADMIN:
            if ProjectRole.ADMIN == target_role:
                return is_self

            return True

        return False

    