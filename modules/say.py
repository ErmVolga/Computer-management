from aiogram.types import Message, CallbackQuery, ForceReply
from aiogram.filters import Command
from aiogram import Dispatcher, F
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

# 💬 Команда /say вручную
async def say_command_handler(message: Message):

    text = message.text.removeprefix("/say").strip()
    if not text:
        await message.answer("📝 Введите текст: <code>/say Привет, мир!</code>")
        return

    threading.Thread(target=speak_text, args=(text,), daemon=True).start()
    await message.answer("🗣️ Озвучиваю...")
    logger.info(f"🗣️ Текст озвучен: {text}")

# 🔘 Кнопка «Сказать» → запрос ввода
async def say_callback(callback: CallbackQuery):

    await callback.message.answer(
        "🗣️ Что сказать?",
        reply_markup=ForceReply(selective=True)
    )
    await callback.answer()

# 📩 Ответ на ForceReply
async def say_reply_handler(message: Message):
    if not message.reply_to_message or "Что сказать?" not in message.reply_to_message.text:
        return

    text = message.text.strip()
    if not text:
        await message.answer("⚠️ Пустой текст.")
        return

    threading.Thread(target=speak_text, args=(text,), daemon=True).start()
    await message.answer("🗣️ Сказано.")
    logger.info(f"🗣️ Озвучено из ForceReply: {text}")

def register(dp: Dispatcher):
    dp.message.register(say_command_handler, Command("say"))
    dp.callback_query.register(say_callback, F.data == "say")
    dp.message.register(say_reply_handler)
