# Computer-management

---


# 🖥️ ErmVolga Computer Management Bot

**Computer Management** — это Telegram-бот на Python, позволяющий управлять своим компьютером через Telegram: запуск, выключение, скриншоты, и многое другое.

---

## 📦 Структура проекта

```
computer-management/
├── main.py                  # Точка входа
├── .env                     # Переменные окружения (токен и ID)
├── bot/
│   ├── config.py            # Загрузка переменных окружения
│   ├── core.py              # Запуск бота и регистрация команд
│   ├── logger.py            # Настройка логирования
│   └── handlers/            # (опционально) отдельные хендлеры
├── modules/                 # Расширяемые модули (например, screenshot)
├── shared/                  # Общие системные утилиты
├── logs/                    # Файлы логов (создаются автоматически)
│   ├── bot_info.log         # INFO и WARNING
│   └── bot_errors.log       # ERROR и CRITICAL
└── requirements.txt         # Зависимости
```

---

## 🚀 Запуск

1. Установи зависимости:

   ```bash
   pip install -r requirements.txt
   ```

2. Создай файл `.env` в корне:

   ```dotenv
   BOT_TOKEN=твой_токен_бота
   ALLOWED_USER_ID=твой_telegram_id
   ```

3. Запусти бота:

   ```bash
   python main.py
   ```

---

## 🛠 Возможности (будут добавляться)

* `/start` — запускает бота, работает только для владельца
* `/screenshot` — сделает скриншот и отправит в Telegram
* `/shutdown` — выключает компьютер
* `/reboot` — перезагружает компьютер
* `/lock` — блокирует экран
* `/say <текст>` — проговаривает текст через голос Windows
* `/open <url>` — открывает сайт в браузере
* `/run <app>` — запускает указанное приложение
* `/status` — отправляет информацию о загрузке CPU, RAM, дисках
* `/webcam` — делает снимок с веб-камеры и отправляет
* `/apps` — показывает список запущенных процессов
* `/kill <name>` — завершает указанный процесс
* `/mic_off` — отключает микрофон (если возможно)
* `/help` — справка по командам

---

📌 Все команды будут реализовываться как **модули в папке `modules/`** — легко добавляются, легко отключаются, не трогая ядро бота.


---

## 🔌 Модули и расширение

Новые функции можно добавлять через модульную систему:

1. Создай файл в `modules/`, например `example.py`
2. Внутри определи `register(dp: Dispatcher)` и подключи свои хендлеры
3. Они автоматически подгрузятся при старте

**Пример:**

```python
# modules/example.py
from aiogram import types, Dispatcher

async def test(message: types.Message):
    await message.answer("Это модуль.")

def register(dp: Dispatcher):
    dp.message.register(test, commands=["test"])
```

---

## 📄 Логирование

* Все события INFO/WARNING записываются в `logs/bot_info.log`
* Ошибки — в `logs/bot_errors.log`
* Автоматическая ротация файлов включена

---