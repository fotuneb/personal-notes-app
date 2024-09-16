# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_note():
    response = client.post("/notes/", json={"title": "Test Note", "content": "This is a test note"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Note"

def test_rate_limit():
    for _ in range(6):  # Assuming rate limit is 5 requests per minute
        response = client.get("/")
        if response.status_code == 429:
            break
    assert response.status_code == 429
