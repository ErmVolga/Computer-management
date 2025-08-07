from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_volume_keyboard(current: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data="volume_down"),
            InlineKeyboardButton(text=f"{current}%", callback_data="volume_show"),
            InlineKeyboardButton(text="➕", callback_data="volume_up")
        ],
        [
            InlineKeyboardButton(text="🔇 Переключить звук", callback_data="volume_toggle_mute")
        ]
    ])