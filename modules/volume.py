from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from shared.system import is_allowed_user_id
from bot.logger import logger
from shared.keyboards.volume import get_volume_keyboard

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))


def get_current_volume() -> int:
    volume = get_volume_interface()
    level = volume.GetMasterVolumeLevelScalar()
    return int(level * 100)


def change_volume(delta_percent: int) -> int:
    volume = get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar()
    new_level = min(1.0, max(0.0, current + delta_percent / 100))
    volume.SetMasterVolumeLevelScalar(new_level, None)
    return int(new_level * 100)


def toggle_mute() -> str:
    volume = get_volume_interface()
    mute_state = volume.GetMute()
    volume.SetMute(not mute_state, None)
    return "🔇 Без звука" if not mute_state else "🔊 Звук включён"


# 💬 Команда /volume
async def volume_handler(message: Message):
    user_id = str(message.from_user.id)
    if not is_allowed_user_id(user_id):
        await message.answer("⛔ У вас нет доступа.")
        return

    vol = get_current_volume()
    await message.answer(f"🔊 Текущая громкость: {vol}%", reply_markup=get_volume_keyboard(vol))


# 🔘 Колбэк
async def volume_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    if not is_allowed_user_id(user_id):
        await callback.answer("⛔ Нет доступа.")
        return

    action = callback.data
    try:
        if action == "volume_up":
            vol = change_volume(+10)
        elif action == "volume_down":
            vol = change_volume(-10)
        elif action == "volume_toggle_mute":
            result = toggle_mute()
            await callback.message.edit_text(result, reply_markup=get_volume_keyboard(get_current_volume()))
            await callback.answer("✅")
            return
        elif action == "volume_show":
            vol = get_current_volume()
        else:
            await callback.answer("⚠️ Неизвестное действие")
            return

        await callback.message.edit_text(f"🔊 Текущая громкость: {vol}%", reply_markup=get_volume_keyboard(vol))
        await callback.answer("✅")

    except Exception as e:
        logger.error(f"❌ Ошибка громкости: {e}")
        await callback.answer("⚠️ Ошибка при изменении громкости")


def register(dp: Dispatcher):
    dp.message.register(volume_handler, Command("volume"))
    dp.callback_query.register(volume_callback, F.data.in_({
        "volume_up", "volume_down", "volume_toggle_mute", "volume_show"
    }))