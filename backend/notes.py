from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.notes import Note,NoteCreate,NoteUpdate,NoteResponse  # Adjust the import based on your project structure
from typing import List

def add_note_to_db(note: NoteCreate, db: Session) -> NoteResponse:
    db_note = Note(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return NoteResponse(id=db_note.id, title=db_note.title, description=db_note.description, completed=db_note.completed, created_time=db_note.created_time)

def update_note_in_db(note_id: int, updated_note: NoteCreate, db: Session) -> NoteResponse:
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    for key, value in updated_note.dict().items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return NoteResponse(id=db_note.id, title=db_note.title, description=db_note.description, completed=db_note.completed, created_time=db_note.created_time)

def delete_note_from_db(note_id: int, db: Session):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted"}

def list_notes_from_db(db: Session) -> List[NoteResponse]:
    return db.query(Note).all()

def get_note_from_db(note_id: int, db: Session) -> NoteResponse:
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteResponse(**db_note.dict())