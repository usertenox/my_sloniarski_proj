from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, func, DateTime
from uuid import UUID, uuid4
from datetime import datetime

from src.models.base import Base
from src.models.mixins import IdPrimaryKey, CreatedAtMixin, UpdatedAtMixin


class Project(IdPrimaryKey, CreatedAtMixin, UpdatedAtMixin, Base):

    __tablename__ = "projects"

    owner_id: Mapped[UUID] = mapped_column( # security-sensitive
        ForeignKey(
            "users.id",
            name="fk_projects_users",
            ondelete="RESTRICT", # без удаления проектов нельзя удалить пользователя
        ),
        index=True,
    )

    name: Mapped[str] = mapped_column(String(150))