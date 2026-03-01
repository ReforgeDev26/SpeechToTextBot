# Telegram Бот для перевода голосовых сообщений в текст

Бот анализирует голосовые сообщения, отправленные пользователем в Telegram. Он извлекает из этих сообщений текст на русском языке.

## Возможности

- Извлечение текста
- Поддержка пересылаемых голосовых

## Требования

- Python 3.7+
- Библиотеки из файла requirements.txt
- Токен Telegram бота (получается через @BotFather)
- Установленный ffmpeg

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ReforgeDev26/SpeechToTextBot.git
cd telegram-photo-metadata-bot
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Установите ffmpeg

4. Создайте бота в Telegram через [@BotFather](https://t.me/BotFather) и получите токен

5. Настройте переменную окружения с токеном бота:

**Linux/macOS:**
```bash
export BOT_TOKEN="ваш_токен_бота"
```

**Windows (PowerShell):**
```powershell
$env:BOT_TOKEN="ваш_токен_бота"
```

**Windows (CMD):**
```cmd
set BOT_TOKEN=ваш_токен_бота
```
## Установка FFmpeg

### Windows

**Автоматическая установка:**
```bash
# Через winget (встроенный менеджер пакетов)
winget install ffmpeg

# Через Chocolatey
choco install ffmpeg
```

Ручная установка:

Скачайте FFmpeg с gyan.dev (выберите ffmpeg-release-essentials.zip)

Распакуйте архив в C:\ffmpeg

Добавьте C:\ffmpeg\bin в переменную PATH:

Нажмите Win + R → sysdm.cpl → Дополнительно → Переменные среды

Найдите Path → Изменить → Создать → Вставьте C:\ffmpeg\bin

Нажмите ОК во всех окнах

### macOS
```bash
# Через Homebrew
brew install ffmpeg
```
### Linux
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```
Проверка установки
```bash
ffmpeg -version
```
## Запуск

```bash
python bot.py
```

## Использование

1. Запустите бота командой `/start`
2. Отправьте боту голосовое сообщение
3. Бот ответит сообщением с извлеченным текстом

## Постоянный запуск на сервере

Для запуска бота на сервере в фоновом режиме можно использовать различные методы:

### Использование systemd (Linux)

1. Создайте файл службы `/etc/systemd/system/SpeechToTextBot.service`:

```ini
[Unit]
Description=Telegram Speech To Text Bot
After=network.target

[Service]
User=ваш_пользователь
WorkingDirectory=/путь/к/боту
Environment="BOT_TOKEN=ваш_токен_бота"
ExecStart=/путь/к/python /путь/к/боту/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Включите и запустите службу:

```bash
sudo systemctl enable SpeechToTextBot
sudo systemctl start SpeechToTextBot
```

## Лицензия


MIT
