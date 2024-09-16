# Dockerfile для FastAPI
FROM python:3.11.9

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости в контейнер
COPY ./requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Копируем весь проект
COPY . /app

# Команда для запуска FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Dockerfile для Telegram-бота
FROM python:3.11.9

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости в контейнер
COPY ./requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Копируем все файлы проекта
COPY . /app

# Команда для запуска Telegram-бота
CMD ["python", "app/bot/main.py"]
