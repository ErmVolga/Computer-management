import pyautogui
from io import BytesIO

def take_screenshot_bytes() -> bytes:
    screenshot = pyautogui.screenshot()
    buf = BytesIO()
    screenshot.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()
