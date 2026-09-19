from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

from src.core.enums import ProjectRole


class MemberCreate(BaseModel):
    user_id: UUID
    role: ProjectRole


class MemberRoleUpdate(BaseModel):
    role: ProjectRole


class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: UUID
    user_id: UUID
    role: ProjectRole
    created_at: datetime