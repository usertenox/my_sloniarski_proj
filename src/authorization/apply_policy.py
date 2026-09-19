from sqlalchemy import Select
from typing import Any

from src.authorization.scopes import Scope, ProjectScope
from src.models.project import Project
from src.models.project_member import ProjectMember
from src.models.document import Document

# Select объект-контейнер описания SQL-запроса


def apply_policy(
        stmt: Select[Any],
        scope: Scope,
        model: type[Any],
) -> Select[Any]:
    """Applies a single row-level authorization scope to a SQLAlchemy query"""

    if isinstance(scope, ProjectScope):
        if model is Project:
            return stmt.where(Project.id==scope.project_id)

        if model is ProjectMember:
            return stmt.where(ProjectMember.id==scope.project_id)

        if model is Document:
            return stmt.where(Document.project_id==scope.project_id)
        
        raise RuntimeError(
            f"model is not {model.__name__}"
        )

    raise RuntimeError(
        f"Unsupported scope: {type(scope).__name__}"
    )