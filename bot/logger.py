import logging
from logging.handlers import RotatingFileHandler
import os

# Папка и пути к логам
LOGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

INFO_LOG_PATH = os.path.join(LOGS_DIR, 'bot_info.log')
ERROR_LOG_PATH = os.path.join(LOGS_DIR, 'bot_errors.log')

# Общий формат
LOG_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Обработчик INFO + WARNING
info_handler = RotatingFileHandler(INFO_LOG_PATH, maxBytes=1_000_000, backupCount=3)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# Обработчик ERROR + CRITICAL
error_handler = RotatingFileHandler(ERROR_LOG_PATH, maxBytes=1_000_000, backupCount=3)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# Логгер
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(info_handler)
logger.addHandler(error_handler)
