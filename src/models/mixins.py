from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func


class IdPrimaryKey:
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )


class CreatedAtMixin:
    created_at = Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class UpdatedAtMixin:
    updated_at = Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )