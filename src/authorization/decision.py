from dataclasses import dataclass
from collections.abc import Sequence

from src.core.access.permissions import Permission
from src.authorization.scopes import Scope


@dataclass(frozen=True)
class AuthorizationDecision:
    permission: Permission
    scopes: Sequence[Scope]

