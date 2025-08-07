from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from bot.filters.access_filter import AccessFilter

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
    await message.answer(HELP_TEXT)

def register(dp: Dispatcher):
    dp.message.register(help_handler, Command("help"), AccessFilter())
