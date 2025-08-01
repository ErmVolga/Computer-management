# Computer-management

```
pc_control_bot/
│
├── bot/                     # Основное ядро бота
│   ├── __init__.py
│   ├── handlers/           # Обработчики Telegram-команд
│   │   └── __init__.py
│   ├── core.py             # Запуск бота, диспетчер
│   └── config.py           # Токен, твой Telegram ID и прочие настройки
│
├── modules/                # Все сторонние "моды", скрипты и команды
│   ├── screenshot.py       # Пример: модуль делает скриншот
│   ├── shutdown.py         # Пример: выключает ПК
│   └── <любой_новый>.py    # Новый скрипт добавляется сюда
│
├── shared/                 # Общие утилиты
│   ├── system.py           # Рабочие функции (завершение работы, скриншот и т.д.)
│   └── tools.py            # Общие вспомогательные функции
│
├── .env                    # BOT_TOKEN и ALLOWED_USER_ID
├── main.py                 # Старт приложения
├── requirements.txt
└── README.md
```