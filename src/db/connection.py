from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import settings

engine = create_async_engine( # заставляет SQLAlchemy общаться с базой данных в неблокирующем режиме через asyncio
    settings.database_url,
    echo=False, # при True логирует все SQL statements и параметры в стандартный вывод, обычно его отключают
    pool_size=10,
    max_overflow=5,
    pool_pre_ping=True,
)
# Разные базы данных говорят на разных «диалектах» SQL, движок  переводит код в сырой 
# SQL-запрос, передавая поток драйверу, создает пул соединений 

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False, # ставвят False, потому что SQLAlchemy во время
    # настройки модели превращает User.email в специальный объект — InstrumentedAttribute
    # он может попытаться незаметно выполнить новый SELECT(в theory подробнее)

    # True помечает все объекты в сессии как «устаревшие», даже если мы просто прочитали их select'ом
    # expire_on_commit=False держит в опертивке данные до закрктия сессии
    
    # каждое обращение за данными с помощью sqlalchemy - поход в бд, asyncpg(драйвер бд) всегда возвращает SQLAlchemy кортежи или словари с сырыми данными
    # алхимия запускает процесс, который называется маппингом - трансформацией строк в объекты, 
    # но перед этим проверяет свой внутренний кэш сессии, который называется Identity Map
    # ключ - составной кортеж из (Класс_Модели, Первичный_Ключ)
    # при создании объекта использует низкоуровневый метод класса __new__
    # объеты Py хранят атрибуты в __dict__, QLAlchemy пихает туда сырые данные - это и есть Mapping

    autoflush=False,
    # autoflush подкидывает изменения в бд, но не закрывает транзакцию(в отличие от commit())
    # это по сути запрос в бд, а нам нужно чтобы изменения все были учетны строго после коммита(и по await)
    # session.close() не коммитит изменения а rollbackает()
)


async def close_db_connections() -> None:
    await engine.dispose()
# запрос уровня приложения

