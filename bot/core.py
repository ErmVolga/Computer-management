from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import Command

from bot.config import BOT_TOKEN, ALLOWED_USER_ID
from bot.logger import logger

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Хендлер /start
async def start_handler(message: Message):
    user_id = str(message.from_user.id)

    if user_id != ALLOWED_USER_ID:
        await message.answer("⛔ У вас нет доступа к этому боту.")
        return

    await message.answer("👋 Бот запущен. Готов к работе.")

dp.message.register(start_handler, Command("start"))

# Запуск
def run_bot():
    import asyncio

    async def main():
        logger.info("🚀 Бот запускается...")
        await dp.start_polling(bot)

    asyncio.run(main())



