import logging
import asyncio
from aiogram import Bot, Dispatcher
from app.bot.config import settings
from app.bot.handlers import start_command, list_notes, create_note_command, search_by_tag
from logging.handlers import TimedRotatingFileHandler

# Настройка логирования
handler = TimedRotatingFileHandler("logs/bot.log", when="midnight", interval=1)
handler.suffix = "%Y-%m-%d"
logging.basicConfig(level=logging.INFO, handlers=[handler])

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

# Привязка команд к обработчикам
dp.message(start_command, commands=["start"])
dp.message(list_notes, commands=["notes"])
dp.message(create_note_command, commands=["create"])
dp.message(search_by_tag, commands=["search"])

# Логируем запуск бота
logging.info("Запуск Telegram-бота")

if __name__ == "__main__":
    try:
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        logging.error(f"Ошибка в боте: {e}")
