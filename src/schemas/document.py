from uuid import UUID
from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, ConfigDict, StringConstraints


DocTitle = Annotated[
    str, 
    StringConstraints(
        strip_whitespace=True, 
        min_length=1, 
        max_length=200
    )
]


DocContent = Annotated[
    str,
    StringConstraints(
        max_length=100_000,
    ),
]


class DocumentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: DocTitle
    content: DocContent


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    created_by_id: UUID
    title: DocTitle
    content: str
    created_at: datetime
    updated_at: datetime | None


class DocumentUpdate(BaseModel):
    title: DocTitle | None  # опциональные(nullable)
    content: DocContent | None = None