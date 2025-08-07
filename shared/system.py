import pyautogui
from io import BytesIO
from bot.config import ALLOWED_USERS

# 🖼 Скриншот
def take_screenshot_file(path="screenshot.png") -> str:
    pyautogui.screenshot(path)
    return path


# 🎙 Состояние микрофона (в оперативной памяти)
MIC_STATE = {"enabled": True}

def is_mic_enabled():
    return MIC_STATE["enabled"]

def set_mic_enabled(state: bool):
    MIC_STATE["enabled"] = state

def is_allowed_user_id(user_id):
    return str(user_id) in ALLOWED_USERS