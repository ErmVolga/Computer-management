from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Dispatcher
from shared.system import is_allowed_user_id
from bot.logger import logger

import threading
import pyttsx3


def speak_text(text: str):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logger.error(f"❌ Ошибка синтеза речи: {e}")


async def say_handler(message: Message):
    user_id = str(message.from_user.id)

    if is_allowed_user_id(user_id):
        await message.answer("⛔ У вас нет доступа к этой команде.")
        return

    text = message.text.removeprefix("/say").strip()

    if not text:
        await message.answer("ℹ️ Использование: <code>/say Привет, мир!</code>")
        return

    try:
        threading.Thread(target=speak_text, args=(text,), daemon=True).start()
        await message.answer("🗣️ Озвучиваю...")
        logger.info(f"🗣️ Текст озвучен: {text}")
    except Exception as e:
        logger.error(f"❌ Ошибка команды /say: {e}")
        await message.answer("⚠️ Не удалось озвучить текст.")


def register(dp: Dispatcher):
    dp.message.register(say_handler, Command("say"))
