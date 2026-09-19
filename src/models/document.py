from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, func, DateTime, String, Text

from src.models.base import Base
from src.models.mixins import IdPrimaryKey, CreatedAtMixin, UpdatedAtMixin


class Document(IdPrimaryKey, CreatedAtMixin, UpdatedAtMixin, Base):

    __tablename__ = "documents"

    project_id: Mapped[UUID] = mapped_column( 
            ForeignKey(
                "projects.id",
                name="fk_document_projects",
                ondelete="CASCADE",
            ),
            index=True,
        )

    created_by_id: Mapped[UUID] = mapped_column( 
            ForeignKey(
                "users.id",
                name="fk_document_user",
                ondelete="RESTRICT",
            ),
        )

    title: Mapped[str] = mapped_column(String(200))

    content: Mapped[str] = mapped_column(Text)