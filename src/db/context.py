from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connection import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
#             get_db создаёт session
# -> отдаёт её в UserRepository
# -> UserRepository попадает в AuthService
# -> endpoint вызывает service.login()
# потом Ошибка начинает подниматься вверх
            await session.rollback()
            raise # тут не надо описывать ошибку, потому что если она и будет на этом уровне
        # то это очко, значит отъебнула бд и это и так понятно будет, + SQLAlchemy уже даст нормальный тип ошибки
       
        # finally:
        #     await session.close()
