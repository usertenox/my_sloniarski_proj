

from src.authorization.context import ProjectAccessContext
from src.authorization.permissions import Permission
from src.authorization.decision import AuthorizationDecision
from src.authorization.scopes import ProjectScope
from src.utils.errors import AccessDenied
from src.authorization.role_permissions import ROLE_PERMISSIONS


class ProjectAuthorizer:
    """Makes access decision. Takes ProjectAccessContext,
    Permission and check owner/role ->
    AuthorizationDecision/AccessDenied"""

    def authorize(
            self,
            permission: Permission,
            context: ProjectAccessContext,
    ) -> AuthorizationDecision:

        if context.is_owner:
            return AuthorizationDecision(
                permission=permission,
                scopes=ProjectScope(project_id=context.project_id), # tuple вернем
            )

        role_permissions = ROLE_PERMISSIONS.get(context.role)

        if role_permissions is None:
            raise AccessDenied()

        if permission not in role_permissions:
            raise AccessDenied()
        
        return AuthorizationDecision(
            permission=permission,
            scopes=ProjectScope(context.project_id),
        )
