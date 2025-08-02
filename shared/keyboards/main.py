from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📸 Screenshot", callback_data="screenshot")],
    [InlineKeyboardButton(text="🖥 Status", callback_data="status")],
    [InlineKeyboardButton(text="📷 Webcam", callback_data="webcam")],
    [
        InlineKeyboardButton(text="⏻ Shutdown", callback_data="shutdown"),
        InlineKeyboardButton(text="🔁 Reboot", callback_data="reboot"),
        InlineKeyboardButton(text="🔒 Lock", callback_data="lock")
    ],
    [InlineKeyboardButton(text="📃 Apps", callback_data="apps")],
    [InlineKeyboardButton(text="🔇 Mic Off", callback_data="mic_off")],
])
