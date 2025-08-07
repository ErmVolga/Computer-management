from aiogram import Dispatcher
from aiogram.types import Message
import psutil
from bot.logger import logger
from aiogram.filters import Command
from bot.filters.access_filter import AccessFilter

async def kill_handler(message: Message):

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ Укажите PID или имя процесса.\nПример: /kill 1234 или /kill notepad.exe")
        return

    target = args[1].strip()
    killed = []

    try:
        if target.isdigit():
            pid = int(target)
            psutil.Process(pid).kill()
            killed.append(f"✅ PID {pid}")
        else:
            for p in psutil.process_iter(['pid', 'name']):
                if p.info['name'].lower() == target.lower():
                    p.kill()
                    killed.append(f"✅ {p.info['name']} (PID {p.info['pid']})")

        if killed:
            await message.answer("\n".join(killed))
        else:
            await message.answer("⚠️ Процесс не найден.")
    except Exception as e:
        logger.error(f"❌ Ошибка в /kill: {e}")
        await message.answer("⚠️ Не удалось завершить процесс.")

def register(dp: Dispatcher):
    dp.message.register(kill_handler, Command("kill"), AccessFilter())