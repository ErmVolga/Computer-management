from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery
from bot.logger import logger
from shared.tools import format_bytes
from bot.filters.access_filter import AccessFilter
import psutil
import time
import datetime


# 🕒 Получить аптайм
def get_uptime_str() -> str:
    boot_time = psutil.boot_time()
    now = time.time()
    delta = datetime.timedelta(seconds=int(now - boot_time))
    return str(delta)


# 📊 Получить статус системы
def get_system_status() -> str:
    # 🌡 CPU: общее и по ядрам
    cpu_total = psutil.cpu_percent(interval=1)
    cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
    cpu_cores = "\n".join(
        f"   • Ядро {i + 1}: {core}%" for i, core in enumerate(cpu_per_core)
    )

    # 💾 RAM
    ram = psutil.virtual_memory().percent

    # 🗂 Диск
    disk_used = psutil.disk_usage("/").percent

    # 📡 Диск: I/O скорость за секунду
    io_before = psutil.disk_io_counters()
    time.sleep(1)
    io_after = psutil.disk_io_counters()

    read_speed = io_after.read_bytes - io_before.read_bytes
    write_speed = io_after.write_bytes - io_before.write_bytes

    # 🌐 Сеть: вход/выход за секунду
    net_before = psutil.net_io_counters()
    time.sleep(1)
    net_after = psutil.net_io_counters()

    recv_speed = (net_after.bytes_recv - net_before.bytes_recv)
    send_speed = (net_after.bytes_sent - net_before.bytes_sent)

    # ⏱ Аптайм
    uptime = datetime.timedelta(seconds=int(time.time() - psutil.boot_time()))

    # 📊 Формируем ответ
    return (
        f"<b>📊 Системная информация:</b>\n\n"
        f"🧠 CPU нагрузка (общая): <b>{cpu_total:.1f}%</b>\n"
        f"{cpu_cores}\n\n"
        f"💾 RAM использование: <b>{ram:.1f}%</b>\n"
        f"🗂 Диск занят: <b>{disk_used:.1f}%</b>\n"
        f"⚙️ Диск: <b>{format_bytes(read_speed)}/s чтение</b>, "
        f"<b>{format_bytes(write_speed)}/s запись</b>\n"
        f"🌐 Сеть: <b>{format_bytes(recv_speed)}/s вход</b>, "
        f"<b>{format_bytes(send_speed)}/s выход</b>\n"
        f"⏱ Аптайм: <b>{uptime}</b>"
    )


# 🔘 Callback
async def status_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)

    try:
        status_text = get_system_status()
        await callback.message.answer(status_text)
        await callback.answer("✅ Готово")
        logger.info(f"📊 Статус отправлен пользователю {user_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка при получении статуса: {e}")
        await callback.answer("⚠️ Не удалось получить статус")


# 📌 Регистрация
def register(dp: Dispatcher):
    dp.callback_query.register(status_callback, F.data == "status", AccessFilter())
