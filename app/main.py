from fastapi import FastAPI, Request, Depends
from app.routers import notes, auth
from app.database import engine
from app import models
from app.logging_config import setup_logging
import logging
from fastapi.responses import JSONResponse, HTMLResponse
from slowapi.middleware import SlowAPIMiddleware
from app.rate_limiter import limiter
from slowapi.errors import RateLimitExceeded

# app/main.py
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.schemas import NoteCreate
from app.crud import get_notes_from_db, create_note_in_db

# Создание таблиц
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Применение Middleware для лимитирования запросов
app.add_middleware(SlowAPIMiddleware, limiter=limiter)

# Подключение маршрутов
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(auth.router, tags=["auth"])  

# Инициализация логирования
setup_logging()

@app.get("/", response_class=HTMLResponse)
async def read_notes(request: Request):
    notes = get_notes_from_db()
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})

@app.post("/notes/")
async def create_note(note: NoteCreate):
    create_note_in_db(note)
    return {"message": "Note created successfully"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Необработанная ошибка: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера"}
    )
    
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Слишком много запросов, попробуйте позже."}
    )

@app.get("/")
@limiter.limit("5/minute")  # Ограничиваем 5 запросами в минуту
async def read_root():
    logging.info("Получен запрос на главную страницу")
    return {"message": "Welcome to the Notes API!"}

@app.get("/notes")
@limiter.limit("10/minute")  # Ограничиваем 10 запросами в минуту
async def get_notes(request: Request):
    # Ваш код получения заметок
    pass