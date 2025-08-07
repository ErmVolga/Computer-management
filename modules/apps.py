from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from bot.logger import logger
import psutil
from shared.tools import format_bytes
from aiogram.filters import Command
from bot.filters.access_filter import AccessFilter


# 🧮 Группировка по критерию
def get_top_processes(metric: str = "cpu", count: int = 5) -> str:
    procs = []

    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'io_counters']):
        try:
            info = p.info
            cpu = info['cpu_percent'] or 0
            mem = info['memory_percent'] or 0
            io = info['io_counters']
            disk = format_bytes((io.read_bytes + io.write_bytes)) if io else "0 B"

            procs.append({
                "name": info['name'] or "??",
                "pid": info['pid'],
                "cpu": cpu,
                "mem": mem,
                "disk": disk
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    key = "cpu" if metric == "cpu" else "mem" if metric == "ram" else "disk"
    procs.sort(key=lambda p: p[key], reverse=True)
    top = procs[:count]

    text = f"<b>📊 Топ {count} процессов по {metric.upper()}:</b>\n\n"
    for p in top:
        text += (
            f"• <b>{p['name']}</b> (PID {p['pid']})\n"
            f"  CPU: {p['cpu']:.1f}% | RAM: {p['mem']:.1f}% | Disk: {p['disk']}\n\n"
        )

    return text


# 🔤 Список всех GUI-приложений (эмуляция)
def get_applications() -> str:
    apps = []

    for p in psutil.process_iter(['pid', 'name', 'username', 'terminal']):
        try:
            name = p.info['name']
            pid = p.info['pid']
            term = p.info['terminal']  # None у фоновых
            if term is not None or 'chrome' in name.lower() or 'explorer' in name.lower():
                apps.append((name, pid))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    apps.sort()
    text = "<b>🔤 Приложения:</b>\n"
    for name, pid in apps:
        text += f"• {name} (PID {pid})\n"

    return text or "⚠️ Нет активных GUI-приложений."


# 💬 /apps <метрика> <кол-во>
async def apps_handler(message: Message):

    args = message.text.split()[1:]
    metric = "cpu"
    count = 5

    if args:
        if args[0] in ("cpu", "ram", "disk"):
            metric = args[0]
        elif args[0] == "gui":
            await message.answer(get_applications())
            return

    if len(args) >= 2 and args[1].isdigit():
        count = int(args[1])

    try:
        text = get_top_processes(metric, count)
        await message.answer(text)
    except Exception as e:
        logger.error(f"❌ Ошибка в /apps: {e}")
        await message.answer("⚠️ Ошибка получения списка процессов.")


# 🔘 Callback (например, с клавиатуры)
async def apps_callback(callback: CallbackQuery):

    try:
        text = get_top_processes()
        await callback.message.answer(text)
        await callback.answer("✅")
    except Exception as e:
        logger.error(f"❌ Callback apps: {e}")
        await callback.answer("⚠️ Ошибка")


def register(dp: Dispatcher):
    dp.message.register(apps_handler, Command("apps"), AccessFilter())
    dp.callback_query.register(apps_callback, F.data == "apps", AccessFilter())
