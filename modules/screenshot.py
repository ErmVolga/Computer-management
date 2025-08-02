from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command
from aiogram import Dispatcher, F
from shared.system import take_screenshot_bytes, is_allowed_user_id
from bot.logger import logger


# 📸 Унифицированная логика отправки скрина
async def send_screenshot(chat, user_id: str):
    try:
        image_bytes = take_screenshot_bytes()
        photo = BufferedInputFile(image_bytes, filename="screenshot.png")
        await chat.answer_photo(photo=photo)
        logger.info(f"📸 Скриншот отправлен пользователю {user_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка скриншота: {e}")
        await chat.answer("⚠️ Не удалось сделать скриншот.")


# 💬 Команда /screenshot
async def screenshot_handler(message: Message):
    user_id = str(message.from_user.id)

    if is_allowed_user_id(user_id):
        await message.answer("⛔ У вас нет доступа.")
        return

    await send_screenshot(message, user_id)


# 🔘 Callback screenshot
async def screenshot_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)

    if is_allowed_user_id(user_id):
        await callback.answer("⛔ Нет доступа.")
        return

    await send_screenshot(callback.message, user_id)
    await callback.answer("✅ Готово")


def register(dp: Dispatcher):
    dp.message.register(screenshot_handler, Command("screenshot"))
    dp.callback_query.register(screenshot_callback, F.data == "screenshot")
