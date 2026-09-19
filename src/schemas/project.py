from typing import Annotated
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, StringConstraints, ConfigDict


ProjectName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=150),
]


class ProjectCreate(BaseModel):
    name: ProjectName
    # без owner,чтобы не было подмены, он задаётся сервером из current_user


class ProjectResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    name: ProjectName
    created_at: datetime
    updated_at: datetime | None


class ProjectUpdate(BaseModel):
    name: ProjectName