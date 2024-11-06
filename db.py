# database.py
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import asyncio
# URL для подключения к базе данных PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL', "postgresql+asyncpg://myuser:mypassword@localhost:5432/mydb")

# Создание асинхронного двигателя SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание фабрики для сессий
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовая модель для ORM
Base = declarative_base()

# Функция для инициализации базы данных
async def init_db():
    async with engine.begin() as conn:
        # Создание всех таблиц, если они еще не существуют
        await conn.run_sync(Base.metadata.create_all)

# Функция для получения сессии, которую можно использовать в зависимостях
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session

