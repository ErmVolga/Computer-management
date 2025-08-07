from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Dispatcher, F
from shared.system import is_allowed_user_id
from bot.logger import logger
import subprocess

# 🔌 Логика выключения
def execute_shutdown():
    try:
        subprocess.Popen("shutdown /s /t 0", shell=True)
        logger.info("⏻ Выключение компьютера запущено.")
    except Exception as e:
        logger.error(f"❌ Ошибка выключения: {e}")
        raise

# 💬 Команда /shutdown
async def shutdown_command(message: Message):
    user_id = str(message.from_user.id)

    if not is_allowed_user_id(user_id):
        await message.answer("⛔ У вас нет доступа к этой команде.")
        return

    try:
        execute_shutdown()
        await message.answer("⏻ Выключаю компьютер...")
    except:
        await message.answer("⚠️ Не удалось выполнить выключение.")

# 🔘 Callback shutdown
async def shutdown_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)

    if not is_allowed_user_id(user_id):
        await callback.answer("⛔ Нет доступа.")
        return

    try:
        execute_shutdown()
        await callback.message.answer("⏻ Выключаю компьютер...")
        await callback.answer("✅")
    except:
        await callback.answer("⚠️ Ошибка выключения")

# 📌 Регистрация
def register(dp: Dispatcher):
    dp.message.register(shutdown_command, Command("shutdown"))
    dp.callback_query.register(shutdown_callback, F.data == "shutdown")