import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# список разрешённых пользователей
ALLOWED_USERS = [uid.strip() for uid in os.getenv("ALLOWED_USERS", "").split(",") if uid.strip()]
