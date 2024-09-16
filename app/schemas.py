# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: list[str] = []

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: list[str]
    created_at: str
    updated_at: str

class NoteBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []

class NoteUpdate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    notes: List[Note] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
