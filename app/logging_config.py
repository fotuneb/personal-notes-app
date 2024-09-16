# app/logging_config.py
import logging
from logging.handlers import TimedRotatingFileHandler

# Создаем кастомный обработчик для ротации логов
def setup_logging():
    handler = TimedRotatingFileHandler("logs/app.log", when="midnight", interval=1)
    handler.suffix = "%Y-%m-%d"
    logging.basicConfig(level=logging.INFO, handlers=[handler])

    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)  # Чтобы отделить логи ошибок
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)  # Логи запросов
