from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Dispatcher
from shared.system import is_allowed_user_id
from bot.logger import logger

async def say_handler(message: Message):
    user_id = str(message.from_user.id)

    if is_allowed_user_id(user_id):
        await message.answer("⛔ У вас нет доступа к этой команде.")
        return

    try:
        pass
    except Exception as e:
        pass


def register(dp: Dispatcher):
    dp.message.register(say_handler, Command("say"))

