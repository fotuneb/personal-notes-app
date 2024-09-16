import httpx
from app.bot.config import settings
import logging

async def register_user(telegram_id: str, username: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.api_url}/auth/register", json={
            "username": username,
            "email": f"{telegram_id}@telegram.com",
            "password": "default_password"  # можно сделать генерацию пароля
        })
        return response.json()

async def get_token(telegram_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.api_url}/auth/token", data={
            "username": f"{telegram_id}@telegram.com",
            "password": "default_password"
        })
        return response.json().get("access_token")

async def get_notes(token: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.api_url}/notes", headers={
                "Authorization": f"Bearer {token}"
            })
            return response.json()
    except Exception as e:
        logging.error(f"Ошибка при получении заметок: {e}")
        return []
    
async def create_note(token: str, title: str, content: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.api_url}/notes", headers={
            "Authorization": f"Bearer {token}"
        }, json={
            "title": title,
            "content": content
        })
        return response.json()

async def search_notes(token: str, tag: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.api_url}/notes?tag={tag}", headers={
            "Authorization": f"Bearer {token}"
        })
        return response.json()
