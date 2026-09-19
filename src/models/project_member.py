from uuid import UUID
from datetime import datetime
from enum import StrEnum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, func, DateTime, Enum

from src.models.base import Base
from src.core.enums import ProjectRole
from src.models.mixins import CreatedAtMixin


class ProjectMember(CreatedAtMixin, Base):

    __tablename__ = "project_members" 

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "projects.id",
            name="fk_project_members_project",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_project_members_users",
            ondelete="CASCADE",
        ),
        primary_key=True,
        index=True,
    )

    role: Mapped[ProjectRole] = mapped_column(
        Enum( # тип данных, задающий набор значений
            ProjectRole,
            native_enum=False, # Колонка как обычная текстовая строка, а не новый тип данных ProjectRole
            name="ck_project_members_role", # имя ограничения - ck 
            create_constraint=True, # создает CHECK
            validate_strings=True, # проверка на уровне py в соответствие ProjectRole, чтобы в базу не кинуть говно, хотя там тоже будет
            # CONSTRAINT ck_project_members_role CHECK (role IN ('admin', 'editor', 'viewer'))
            values_callable=lambda cls_roles: [role.value for role in cls_roles], # это готовит ('admin', 'editor', 'viewer')
        )
    )