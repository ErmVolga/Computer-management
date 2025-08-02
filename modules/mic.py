from aiogram.types import CallbackQuery
from aiogram import Dispatcher, F
from shared.system import is_allowed_user_id, is_mic_enabled, set_mic_enabled
from bot.logger import logger
import subprocess

def toggle_mic(state: bool):
    try:
        device_name = "Microphone"
        command = (
            f'powershell.exe -Command "Get-PnpDevice | '
            f'Where-Object {{ $_.FriendlyName -like \'*{device_name}*\' -and $_.Class -eq \'AudioEndpoint\' }} | '
            f'ForEach-Object {{ Set-PnpDevice -InstanceId $_.InstanceId -Enabled:{str(state).ToLower()} -Confirm:$false }}"'
        )
        subprocess.run(command, shell=True)
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка включения/отключения микрофона: {e}")
        return False

async def mic_toggle_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)

    if is_allowed_user_id(user_id):
        await callback.answer("⛔ Нет доступа.")
        return

    current = is_mic_enabled()
    new_state = not current

    if toggle_mic(new_state):
        set_mic_enabled(new_state)
        text = "🎤 Микрофон включён." if new_state else "🔇 Микрофон отключён."
        await callback.message.edit_reply_markup(reply_markup=callback.message.reply_markup)  # обновим клавиатуру
        await callback.answer("✅ Выполнено.")
        await callback.message.answer(text)
        logger.info(f"🎙 Микрофон переключён: {'включён' if new_state else 'отключён'}")
    else:
        await callback.answer("⚠️ Не удалось изменить состояние микрофона.")

def register(dp: Dispatcher):
    dp.callback_query.register(mic_toggle_callback, F.data == "toggle_mic")
