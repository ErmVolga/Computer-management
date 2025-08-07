from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from shared.system import is_allowed_user_id

HELP_TEXT = """
<b>🧾 Доступные команды:</b>
/start — запуск бота
/status — статус системы
/screenshot — скриншот экрана
/shutdown — выключить ПК
/reboot — перезагрузка
/volume — управление громкостью
/say &lt;текст&gt; — проговорить  
/apps [cpu|ram|disk|gui] [n] — топ процессов
/kill &lt;pid|имя&gt; — завершить процесс
/help — показать справку
"""

async def help_handler(message: Message):
    user_id = str(message.from_user.id)
    if not is_allowed_user_id(user_id):
        await message.answer("⛔ Нет доступа.")
        return
    await message.answer(HELP_TEXT)

def register(dp: Dispatcher):
    dp.message.register(help_handler, Command("help"))
