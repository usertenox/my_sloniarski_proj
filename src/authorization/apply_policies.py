from typing import Any

from sqlalchemy import Select

from src.authorization.apply_policy import apply_policy
from src.authorization.decision import AuthorizationDecision


def apply_policies(
        stmt: Select,
        model: type[Any],
        decision: AuthorizationDecision,
) -> Select[Any]:

    for scope in decision.scopes:
        return apply_policy(
            stmt=stmt,
            scope=scope,
            model=model,
        )