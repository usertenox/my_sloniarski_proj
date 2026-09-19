from uuid import UUID
from datetime import datetime
from src.models.refresh_token import RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update


class RefreshTokenRepo:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_ref_token(
            self,
            jti: UUID,
            user_id: UUID,
            token_hash: str,
            expires_at: datetime,
    ) -> None:
        
        ref_token = RefreshToken(
            jti = jti,
            user_id = user_id,
            token_hash = token_hash,
            expires_at = expires_at, 
        )

        self.db.add(ref_token)

        await self.db.flush()
        await self.db.refresh(ref_token)



    async def get_by_jti_for_update(
            self,
            jti: UUID,
    ) -> RefreshToken | None:

        """ уязвимость называется гонка (Race Condition), т.е 2 одновременных запроса на новый refresh могут создать 2 работающих токена"""

        query = (
            select(RefreshToken)
            .where(RefreshToken.jti==jti).with_for_update()
              # с намерением для обновления, блокает строку до конца транзакции 
        )

        res = await self.db.execute(query)

        return res.scalar_one_or_none()



    """токен можно использовать только один раз - ротация"""

    async def revoke(
            self,
            refresh_token: RefreshToken,
            revoked_at: datetime,
    ) -> None:

        refresh_token.revoked_at = revoked_at

        await self.db.flush()


    async def revoke_all_by_user_id(
            self,
            user_id: UUID,
            revoked_at: datetime,
    ) -> None:

        query = update(RefreshToken).where(
                                        RefreshToken.user_id == user_id,
                                        RefreshToken.revoked_at.is_(None),
                                    ).values(revoked_at=revoked_at)

        await self.db.execute(query)
        

