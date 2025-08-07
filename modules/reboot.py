from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher, F
from bot.logger import logger
from aiogram.filters import Command
from bot.filters.access_filter import AccessFilter
import os
import asyncio

# 🔁 Общая логика перезагрузки
async def reboot_system(chat, user_id: str):
    try:
        await chat.answer("🔁 Перезагрузка компьютера...")
        logger.info(f"🔁 Перезагрузка инициирована пользователем {user_id}")
        await asyncio.sleep(1)  # Небольшая задержка, чтобы успело отправиться сообщение
        os.system("shutdown /r /t 0")  # Windows: перезагрузка немедленно
    except Exception as e:
        logger.error(f"❌ Ошибка перезагрузки: {e}")
        await chat.answer("⚠️ Не удалось перезагрузить компьютер.")

# 💬 Команда /reboot
async def reboot_handler(message: Message):
    user_id = str(message.from_user.id)
    await reboot_system(message, user_id)

# 🔘 Callback reboot
async def reboot_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    await reboot_system(callback.message, user_id)
    await callback.answer("✅ Перезагрузка...")

# 📌 Регистрация
def register(dp: Dispatcher):
    dp.message.register(reboot_handler, Command("reboot"), AccessFilter())
    dp.callback_query.register(reboot_callback, F.data == "reboot", AccessFilter())
