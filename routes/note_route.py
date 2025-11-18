from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database.session import get_db
from models.notes_model import Note

n_router = APIRouter()

class PostNote(BaseModel):
    title: str
    context: Optional[str, None] = None

class GetNote(PostNote):
    created_at: datetime

@n_router.post('/notes', response_model=GetNote)
async def create_note(data: PostNote, db = Depends(get_db)):
    try:
        new_note = Note(title = data.title,
                        context = data.context)
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        return new_note
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере")

@n_router.get('/notes', response_model=List[GetNote])
async def get_notes(db = Depends(get_db)):
    try:
        notes = db.query(Note).all()
        return notes
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере")

@n_router.get('/notes/{note_id}', response_model=GetNote)
async def get_note(note_id: int, db = Depends(get_db)):
    try:
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            raise HTTPException(status_code=404, detail='Не найдено')
        return note
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере")