import random
from typing import Optional, List

from sqlalchemy import Column, Integer, Boolean, select, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from bot.Utils.bd.Base import Base, engine, AsyncSessionLocal


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True, autoincrement=True)
    username = Column(String)
    user_id = Column(BIGINT, unique=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_user(user_id: int, username: str):
    new_user = Users(user_id=user_id, username=username)
    async with AsyncSessionLocal() as session:
        session.add(new_user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()

async def get_all_user_ids() -> List[int]:
    """
    Получает список всех user_id из таблицы Users
    Возвращает список ID или пустой список при ошибке
    """
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Users.user_id)
            )
            user_ids = result.scalars().all()
            return user_ids
        except Exception as e:
            print(f"Ошибка при получении user_ids: {e}")
            return []

async def user_exists(user_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Users).where(Users.user_id == user_id)
            )
            return result.scalar_one_or_none() is not None
        except SQLAlchemyError:
            return False  # можно логировать при необходимости

async def get_info_all_users() -> List[Users]:
    """
    Получает список всех пользователей из таблицы Users
    Возвращает список объектов Users или пустой список при ошибке
    """
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Users)  # Получаем полные объекты, а не только user_id
            )
            users = result.scalars().all()
            return users
        except Exception as e:
            print(f"Ошибка при получении пользователей: {e}")
            return []


