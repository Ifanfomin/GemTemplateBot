# Настройка логирования
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot.config import config

logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Мидлварь для логирования
dp.middleware.setup(LoggingMiddleware())

# Преобразование конфигурации в словарь
config_dict = {
    "BOT_TOKEN": config.BOT_TOKEN
}

# Мидлварь для управления окружением (передача конфигурации как словарь)
dp.middleware.setup(EnvironmentMiddleware(config_dict))

from bot.Handlers import Common, Admins, Users
Common.register_common_handlers(dp)
Admins.register_admins_handlers(dp)
Admins.setup_filters(dp)
Users.register_test_handlers(dp)