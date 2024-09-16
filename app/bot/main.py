import logging
from aiogram import Bot, Dispatcher, executor
from app.bot.config import settings
from app.bot.handlers import start_command, list_notes, create_note_command, search_by_tag
from logging.handlers import TimedRotatingFileHandler

# Настройка логирования
handler = TimedRotatingFileHandler("logs/bot.log", when="midnight", interval=1)
handler.suffix = "%Y-%m-%d"
logging.basicConfig(level=logging.INFO, handlers=[handler])

bot = Bot(token=settings.bot_token)
dp = Dispatcher(bot)

# Привязка команд к обработчикам
dp.register_message_handler(start_command, commands=["start"])
dp.register_message_handler(list_notes, commands=["notes"])
dp.register_message_handler(create_note_command, commands=["create"])
dp.register_message_handler(search_by_tag, commands=["search"])

# Логируем запуск бота
logging.info("Запуск Telegram-бота")

if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logging.error(f"Ошибка в боте: {e}")
