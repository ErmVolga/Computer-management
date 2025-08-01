import logging
from logging.handlers import RotatingFileHandler
import os

# 📂 Папка проекта (корень)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 📁 Папка и пути к логам
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

INFO_LOG_PATH = os.path.join(LOGS_DIR, "bot_info.log")
ERROR_LOG_PATH = os.path.join(LOGS_DIR, "bot_errors.log")

# 🧠 Кастомный форматтер, который добавляет %(relativepath)s
class RelativePathFormatter(logging.Formatter):
    def format(self, record):
        full_path = os.path.abspath(record.pathname)
        record.relativepath = os.path.relpath(full_path, start=PROJECT_ROOT)
        return super().format(record)

# 📝 Формат и дата
LOG_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s  [→ %(relativepath)s]"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 🎯 Фильтры
class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.INFO, logging.WARNING)

class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR

# 🟡 INFO/WARNING Handler
info_handler = RotatingFileHandler(INFO_LOG_PATH, maxBytes=1_000_000, backupCount=3)
info_handler.setLevel(logging.INFO)
info_handler.addFilter(InfoFilter())
info_handler.setFormatter(RelativePathFormatter(LOG_FORMAT, DATE_FORMAT))

# 🔴 ERROR Handler
error_handler = RotatingFileHandler(ERROR_LOG_PATH, maxBytes=1_000_000, backupCount=3)
error_handler.setLevel(logging.ERROR)
error_handler.addFilter(ErrorFilter())
error_handler.setFormatter(RelativePathFormatter(LOG_FORMAT, DATE_FORMAT))

# 📢 Логгер
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(info_handler)
logger.addHandler(error_handler)
