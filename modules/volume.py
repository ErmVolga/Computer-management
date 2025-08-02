from aiogram.types import Message, CallbackQuery, ForceReply
from aiogram.filters import Command
from aiogram import Dispatcher, F
from shared.system import is_allowed_user_id
from bot.logger import logger

from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import re

# 🎛 Установить громкость
def set_volume(percent: int) -> bool:
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка установки громкости: {e}")
        return False

# 💬 Команда /volume [число]
async def volume_command_handler(message: Message):
    user_id = str(message.from_user.id)

    if is_allowed_user_id(user_id):
        await message.answer("⛔ У вас нет доступа.")
        return

    match = re.match(r"/volume\s+(\d+)", message.text)
    if not match:
        await message.answer("ℹ️ Использование: <code>/volume 50</code> (0–100)")
        return

    percent = int(match.group(1))
    if percent < 0 or percent > 100:
        await message.answer("⚠️ Введите число от 0 до 100.")
        return

    if set_volume(percent):
        await message.answer(f"🔊 Громкость установлена на {percent}%")
        logger.info(f"🔊 Громкость изменена пользователем {user_id} на {percent}%")
    else:
        await message.answer("⚠️ Не удалось изменить громкость.")

# 🔘 Кнопка "Громкость" → запрос значения
async def volume_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)

    if is_allowed_user_id(user_id):
        await callback.answer("⛔ Нет доступа.")
        return

    await callback.message.answer(
        "🔊 Введите громкость (0–100):",
        reply_markup=ForceReply(selective=True)
    )
    await callback.answer()

# 📩 Ответ на ForceReply
async def volume_reply_handler(message: Message):
    user_id = str(message.from_user.id)

    if is_allowed_user_id(user_id):
        return

    if not message.reply_to_message or "громкость" not in message.reply_to_message.text.lower():
        return

    text = message.text.strip()
    if not text.isdigit():
        await message.answer("⚠️ Введите число от 0 до 100.")
        return

    percent = int(text)
    if percent < 0 or percent > 100:
        await message.answer("⚠️ Введите число от 0 до 100.")
        return

    if set_volume(percent):
        await message.answer(f"🔊 Громкость установлена на {percent}%")
        logger.info(f"🔊 Громкость установлена через ForceReply: {percent}%")
    else:
        await message.answer("⚠️ Не удалось изменить громкость.")

# 📌 Регистрация
def register(dp: Dispatcher):
    dp.message.register(volume_command_handler, Command("volume"))
    dp.callback_query.register(volume_callback, F.data == "volume")
    dp.message.register(volume_reply_handler)
