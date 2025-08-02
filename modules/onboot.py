from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN, ALLOWED_USER_ID
from aiogram.types import Message
from bot.logger import logger
from shared.keyboards.main import get_main_keyboard

async def notify_on_boot():
    try:
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(
            chat_id=ALLOWED_USER_ID,
            text="✅ Компьютер включён и бот запущен. Готов к работе 💻",
            reply_markup=get_main_keyboard()
        )
        logger.info("📩 Сообщение о включении отправлено пользователю.")
        await bot.session.close()
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке сообщения о запуске: {e}")

def register(dp: Dispatcher):
    dp.startup.register(notify_on_boot)
