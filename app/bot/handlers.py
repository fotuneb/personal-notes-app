# app/bot/handlers.py
from aiogram import types
from aiogram.dispatcher import Dispatcher
from app.bot.api import register_user, get_token, get_notes, create_note, search_notes

# app/bot/handlers.py
import logging
from aiogram import types
from app.bot.api import register_user, get_token, get_notes, create_note, search_notes

async def start_command(message: types.Message):
    await register_user(telegram_id=message.from_user.id, username=message.from_user.username)
    logging.info(f"Пользователь {message.from_user.id} зарегистрирован через Telegram")
    await message.answer("Привет! Ты успешно зарегистрирован в системе заметок!")

async def list_notes(message: types.Message):
    token = await get_token(telegram_id=message.from_user.id)
    notes = await get_notes(token)
    if not notes:
        await message.answer("У тебя пока нет заметок.")
    else:
        notes_list = "\n\n".join([f"Заметка {note['id']}:\n{note['title']}\n{note['content']}" for note in notes])
        logging.info(f"Пользователь {message.from_user.id} запросил список заметок")
        await message.answer(notes_list)

async def create_note_command(message: types.Message):
    token = await get_token(telegram_id=message.from_user.id)
    await message.answer("Введите заголовок заметки:")
    
    @Dispatcher.message_handler(lambda msg: True)
    async def get_title(msg: types.Message):
        title = msg.text
        await message.answer("Введите содержимое заметки:")
        
        @Dispatcher.message_handler(lambda msg: True)
        async def get_content(msg: types.Message):
            content = msg.text
            await create_note(token, title, content)
            await message.answer("Заметка создана!")

async def search_by_tag(message: types.Message):
    token = await get_token(telegram_id=message.from_user.id)
    tag = message.get_args()  # Получаем аргумент команды
    notes = await search_notes(token, tag)
    if not notes:
        await message.answer(f"Заметок с тегом {tag} не найдено.")
    else:
        notes_list = "\n\n".join([f"Заметка {note['id']}:\n{note['title']}\n{note['content']}" for note in notes])
        await message.answer(notes_list)
