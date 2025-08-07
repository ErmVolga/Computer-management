from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Dispatcher, F
from bot.logger import logger
import os
from aiogram.types import FSInputFile
from shared.system import take_screenshot_file
from bot.filters.access_filter import AccessFilter

# 📸 Унифицированная логика отправки скрина
async def send_screenshot(chat, user_id: str):
    try:
        path = take_screenshot_file()
        photo = FSInputFile(path)
        await chat.answer_photo(photo=photo)
        os.remove(path)  # удалим файл
    except Exception as e:
        logger.error(f"❌ Ошибка скриншота: {e}")
        await chat.answer("⚠️ Не удалось сделать скриншот.")


# 💬 Команда /screenshot
async def screenshot_handler(message: Message):
    user_id = str(message.from_user.id)
    await send_screenshot(message, user_id)


# 🔘 Callback screenshot
async def screenshot_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)

    await send_screenshot(callback.message, user_id)
    await callback.answer("✅ Готово")


def register(dp: Dispatcher):
    dp.message.register(screenshot_handler, Command("screenshot"), AccessFilter())
    dp.callback_query.register(screenshot_callback, F.data == "screenshot", AccessFilter())
