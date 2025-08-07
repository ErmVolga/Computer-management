from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import webbrowser

async def open_url_handler(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ Укажите ссылку. Пример: /open https://example.com")
        return
    url = args[1].strip()
    webbrowser.open(url)
    await message.answer(f"🌐 Открываю: {url}")

def register(dp: Dispatcher):
    dp.message.register(open_url_handler, Command("open"))
