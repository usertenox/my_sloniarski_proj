from dataclasses import dataclass
from uuid import UUID

class Scope:
    pass


@dataclass(frozen=True)
class ProjectScope(Scope): # isinstance(obj класса ProjectScope, Scope) -> True
    project_id: UUID