from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import Command

from bot.config import BOT_TOKEN, ALLOWED_USER_ID
from bot.logger import logger

import os
import importlib

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# 🧩 Автоматическая регистрация модулей
def load_modules(dp: Dispatcher):
    modules_dir = os.path.join(os.path.dirname(__file__), '..', 'modules')

    for filename in os.listdir(modules_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"modules.{filename[:-3]}"
            try:
                mod = importlib.import_module(module_name)
                if hasattr(mod, "register"):
                    mod.register(dp)
                    logger.info(f"✅ Модуль '{module_name}' загружен.")
                else:
                    logger.warning(f"⚠️ Модуль '{module_name}' не содержит функцию register(dp)")
            except Exception as e:
                logger.error(f"❌ Ошибка при загрузке модуля '{module_name}': {e}")

# 👤 Хендлер /start (только для ALLOWED_USER_ID)
async def start_handler(message: Message):
    user_id = str(message.from_user.id)

    if user_id != ALLOWED_USER_ID:
        logger.warning(f"🚫 Запрет доступа для пользователя {user_id}")
        await message.answer("⛔ У вас нет доступа к этому боту.")
        return

    logger.info(f"✅ Авторизованный пользователь {user_id} использовал /start")
    await message.answer("👋 Бот запущен. Готов к работе.")

dp.message.register(start_handler, Command("start"))

# 🚀 Запуск
def run_bot():
    import asyncio

    async def main():
        logger.info("🚀 Бот запускается...")
        load_modules(dp)
        await dp.start_polling(bot)

    asyncio.run(main())


