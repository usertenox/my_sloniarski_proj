from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, DateTime
from uuid import UUID
from datetime import datetime
from src.models.mixins import CreatedAtMixin


# Чтобы связать строку из таблицы 1 со строкой из 
# таблицы 2, базе данных физически нужно место, где 
# она запишет, какому объекту 1 принадлежит объект 2, 
# такую колонку создает ForeignKey в дочерней таблице.


class RefreshToken(CreatedAtMixin, Base): # ищем токен по jti при auth, дополнительно сверяем по хэшу 
    __tablename__ = "refresh_tokens"

    jti: Mapped[UUID] = mapped_column(
        primary_key=True, # прм запросе токена поиск одет по jti
    )

    user_id: Mapped[UUID] = mapped_column( 
        ForeignKey(
            'users.id', 
            name='fk_refresh_tokens_user_id',
            ondelete="CASCADE",
        ),
        index=True,
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    # SQLAlchemy загружает «чертежи» из кода в момент запуска приложения.
    # модели автоматически упаковываются в объект-коллекцию — Base.metadata,
    # в alembic/env.py в target_metadata