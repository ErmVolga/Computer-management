import pyautogui
from io import BytesIO
from bot.config import ALLOWED_USER_ID

# 🖼 Скриншот
def take_screenshot_bytes() -> bytes:
    screenshot = pyautogui.screenshot()
    buf = BytesIO()
    screenshot.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()

# 🔒 Проверка доступа
def is_allowed_user_id(user_id):
    return ALLOWED_USER_ID != user_id

# 🎙 Состояние микрофона (в оперативной памяти)
MIC_STATE = {"enabled": True}

def is_mic_enabled():
    return MIC_STATE["enabled"]

def set_mic_enabled(state: bool):
    MIC_STATE["enabled"] = state
