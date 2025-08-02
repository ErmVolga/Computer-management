from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from shared.system import is_mic_enabled

def get_main_keyboard() -> InlineKeyboardMarkup:
    mic_state = is_mic_enabled()

    keyboard = [
        [InlineKeyboardButton(text="📸 Screenshot", callback_data="screenshot")],
        [InlineKeyboardButton(text="🖥 Status", callback_data="status")],
        [InlineKeyboardButton(text="🔊 Громкость", callback_data="volume")],
        [InlineKeyboardButton(text="🎤 Сказать", callback_data="say")],
        [
            InlineKeyboardButton(text="⏻ Выключить", callback_data="shutdown"),
            InlineKeyboardButton(text="🔁 Перезагрузка", callback_data="reboot"),
            InlineKeyboardButton(text="🔒 Блокировка", callback_data="lock")
        ],
        [InlineKeyboardButton(
            text="🔇 Выключить микрофон" if mic_state else "🎤 Включить микрофон",
            callback_data="toggle_mic"
        )]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

main_keyboard = get_main_keyboard()
