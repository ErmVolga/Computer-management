from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command
from aiogram import Dispatcher
from shared.system import take_screenshot_bytes, is_allowed_user_id
from bot.logger import logger

async def screenshot_handler(message: Message):
    user_id = str(message.from_user.id)

    if is_allowed_user_id(user_id):
        await message.answer("⛔ У вас нет доступа к этой команде.")
        return

    try:
        image_bytes = take_screenshot_bytes()
        photo = BufferedInputFile(image_bytes, filename="screenshot.png")
        await message.answer_photo(photo=photo)
        logger.info(f"📸 Скриншот (в памяти) отправлен пользователю {user_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка при создании скриншота: {e}")
        await message.answer("⚠️ Не удалось сделать скриншот.")


def register(dp: Dispatcher):
    dp.message.register(screenshot_handler, Command("screenshot"))

