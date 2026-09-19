from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from src.models.user import User


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_email(self, email: str) -> User | None:
        email_request = select(User).where(User.email==email.lower())
        res_request = await self.db.execute(email_request) 

        return res_request.scalar_one_or_none() 
    
    async def get_by_id(self, user_id: UUID) -> User | None:
        id_request = select(User).where(User.id==user_id)
        res_reqest = await self.db.execute(id_request)

        return res_reqest.scalar_one_or_none()
    
    async def create(self, username: str, email: str, password_hash: str) -> User:

        user = User(
            username=username,
            email=email.lower(),
            password_hash=password_hash,
        )
        
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)

        return user