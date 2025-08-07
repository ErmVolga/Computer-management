from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery
from shared.system import is_allowed_user_id
from bot.logger import logger
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
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk_used = psutil.disk_usage("/").percent

    # 📡 Нагрузка на диск (изменение I/O за 1 сек)
    io_before = psutil.disk_io_counters()
    time.sleep(1)
    io_after = psutil.disk_io_counters()

    read_speed = (io_after.read_bytes - io_before.read_bytes) / 1024 / 1024  # MB/s
    write_speed = (io_after.write_bytes - io_before.write_bytes) / 1024 / 1024  # MB/s

    uptime = datetime.timedelta(seconds=int(time.time() - psutil.boot_time()))

    return (
        f"<b>📊 Системная информация:</b>\n"
        f"🧠 CPU нагрузка: <b>{cpu}%</b>\n"
        f"💾 RAM использование: <b>{ram}%</b>\n"
        f"🗂 Диск занят: <b>{disk_used}%</b>\n"
        f"⚙️ Нагрузка на диск: <b>{read_speed:.1f} MB/s чтение</b>, <b>{write_speed:.1f} MB/s запись</b>\n"
        f"⏱ Аптайм: <b>{uptime}</b>"
    )


# 🔘 Callback
async def status_callback(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    if is_allowed_user_id(user_id):
        await callback.answer("⛔ Нет доступа.")
        return

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
    dp.callback_query.register(status_callback, F.data == "status")
