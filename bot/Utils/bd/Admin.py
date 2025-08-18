from sqlalchemy import Column, Integer, BIGINT, String, select
from sqlalchemy.exc import IntegrityError

from bot.Utils.bd.Base import Base, engine, AsyncSessionLocal


class Admins(Base):
    __tablename__ = 'admins'

    id = Column(Integer,primary_key=True, autoincrement=True)
    username = Column(String)
    user_id = Column(BIGINT, unique=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_admins(user_id: int, username: str):
    new_user = Admins(user_id=user_id, username=username)
    async with AsyncSessionLocal() as session:
        session.add(new_user)
        try:
            await session.commit()
            return True
        except IntegrityError:
            await session.rollback()

async def if_admins(user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Admins).where(Admins.user_id == user_id))
        user = result.scalar_one_or_none()
        if user:
            return True

