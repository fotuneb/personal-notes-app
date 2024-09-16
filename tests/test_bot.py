# tests/test_bot.py
import pytest
from unittest.mock import AsyncMock, patch
from app.bot.main import dp
from aiogram import types

@pytest.mark.asyncio
async def test_start_command():
    with patch("app.bot.main.register_user", new_callable=AsyncMock) as mock_register_user:
        message = types.Message(chat=types.Chat(id=1), from_user=types.User(id=1, username="test_user"), text="/start")
        await dp.process_updates([types.Update(message=message)])
        mock_register_user.assert_called_once_with(telegram_id=1, username="test_user")
