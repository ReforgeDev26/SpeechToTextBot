import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
import logging
import speech_recognition as sr
from dotenv import load_dotenv
import tempfile
import subprocess
import logging
from ffmpeg_finder import find_ffmpeg


# Загружаем переменные из файла .env
load_dotenv()

# Конфигурация логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")

bot = Bot(token=TOKEN)
dp = Dispatcher()
recognizer = sr.Recognizer()  # Создаем экземпляр класса

FFMPEG_PATH = find_ffmpeg()

async def convert_ogg_to_wav(ogg_path, wav_path):
    """Конвертирует OGG в WAV через ffmpeg"""
    try:
        cmd = [FFMPEG_PATH, '-i', ogg_path, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', wav_path, '-y']
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка конвертации: {e.stderr.decode()}")
        return False

async def get_voice_text(voice: types.Voice) -> str:
    """
    Преобразует голосовое сообщение в текст
    """
    ogg_file_path = None
    wav_file_path = None
    
    try:
        # Получаем информацию о файле
        file_id = voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        
        logging.info(f"Скачиваем файл: {file_path}")
        
        # Создаем временный файл для OGG
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp_ogg:
            await bot.download_file(file_path, tmp_ogg.name)
            ogg_file_path = tmp_ogg.name
            logging.info(f"OGG файл сохранен: {ogg_file_path}")
        
        # Создаем временный файл для WAV
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            wav_file_path = tmp_wav.name
            logging.info(f"WAV файл будет создан: {wav_file_path}")
        
        # Конвертируем OGG в WAV
        if not await convert_ogg_to_wav(ogg_file_path, wav_file_path):
            return "❌ Ошибка при конвертации аудиофайла"
        
        try:
            # Используем speech_recognition для преобразования в текст
            with sr.AudioFile(wav_file_path) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language="ru-RU")
                return text
        except sr.UnknownValueError:
            return "🤔 Не удалось распознать речь"
        except sr.RequestError as e:
            return f"❌ Ошибка сервиса распознавания: {e}"
        finally:
            # Удаляем временный файл
            if os.path.exists(wav_file_path):
                os.remove(wav_file_path)
                
    except Exception as e:
        logging.error(f"Ошибка при обработке голосового сообщения: {e}")
        return f"❌ Произошла ошибка: {str(e)}"

@dp.message(F.voice)
async def handle_voice(message: Message):
    """
    Обработчик голосовых сообщений
    """
    try:
        # Отправляем уведомление о начале обработки
        processing_msg = await message.answer("🔄 Обрабатываю голосовое сообщение...")
        
        # Получаем текст из голосового сообщения
        result = await get_voice_text(message.voice)
        
        # Удаляем сообщение о обработке
        await processing_msg.delete()
        
        # Отправляем результат
        await message.answer(f"📝 Распознанный текст:\n{result}")
        
    except Exception as e:
        logging.error(f"Ошибка в обработчике: {e}")
        await message.answer(f"❌ Произошла ошибка: {str(e)}")

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обработчик команды /start
    """
    await message.answer(
        "👋 Привет! Я бот для распознавания голосовых сообщений.\n\n"
        "Просто отправь мне голосовое сообщение, и я переведу его в текст!"
    )

async def main():
    """
    Запуск бота
    """
    if FFMPEG_PATH:
        print("Бот запущен и готов к работе!")
        await dp.start_polling(bot)
    else:
        print("Не удалось найти ffmpeg")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())