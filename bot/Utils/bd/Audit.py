from sqlalchemy import Column, Integer, BIGINT, String, select
from sqlalchemy.exc import IntegrityError

from bot.Utils.bd.Base import Base, engine, AsyncSessionLocal

class Audit(Base):
    __tablename__ = 'audit'

    id = Column(Integer,primary_key=True, autoincrement=True)
    username = Column(String)
    user_id = Column(BIGINT)
    action = Column(String)
