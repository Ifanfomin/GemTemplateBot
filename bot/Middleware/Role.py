from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from bot.Utils.bd.Admin import if_admins
from bot.config import config

class RoleMiddleware(BaseMiddleware):
    def __init__(self):
        super(RoleMiddleware, self).__init__()

    async def on_process_message(self, message: Message, data: dict):
        user_id = message.from_user.id

        # Проверка, является ли пользователь администратором
        if if_admins(user_id=user_id):
            data['role'] = 'admin'
        else:
            data['role'] = 'user'
