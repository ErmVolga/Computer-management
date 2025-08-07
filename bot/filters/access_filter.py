from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from bot.config import ALLOWED_USERS


class AccessFilter(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return str(event.from_user.id) in ALLOWED_USERS
