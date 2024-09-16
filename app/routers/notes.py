# app/routers/notes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models
from app.database import get_db
from app.auth import get_current_user
from app.crud import create_note
import logging
from app.schemas import NoteCreate, NoteResponse

router = APIRouter()

@router.post("/notes/", response_model=NoteResponse)
async def create_note(note: NoteCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    try:
        new_note = create_note(db, note, user)
        logging.info(f"Заметка '{note.title}' создана пользователем {user}")
        return new_note
    except Exception as e:
        logging.error(f"Ошибка при создании заметки: {str(e)}")
        raise HTTPException(status_code=400, detail="Ошибка при создании заметки")

@router.post("/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_note(db, note, current_user.id)

@router.get("/", response_model=List[schemas.Note])
def get_notes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_notes(db, skip=skip, limit=limit)

@router.put("/{note_id}", response_model=schemas.Note)
def update_note(note_id: int, note_update: schemas.NoteUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    note = crud.get_note_by_id(db, note_id)
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this note")
    return crud.update_note(db, note_id, note_update)

@router.delete("/{note_id}", response_model=schemas.Note)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    note = crud.get_note_by_id(db, note_id)
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")
    return crud.delete_note(db, note_id)
