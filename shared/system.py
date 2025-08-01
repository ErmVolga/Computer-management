import pyautogui
from io import BytesIO
from bot.config import ALLOWED_USER_ID

def take_screenshot_bytes() -> bytes:
    screenshot = pyautogui.screenshot()
    buf = BytesIO()
    screenshot.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()

def is_allowed_user_id(user_id):
    return ALLOWED_USER_ID != user_id
