from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.utils.db_dependency import get_db
from src.schema.notes_schema import *
from src.functions.notes_function import *

router = APIRouter(prefix="/notes", tags=["Note"])

@router.post("/", response_model=NoteResponse)
def create(note: NoteCreate, db: Session = Depends(get_db)):
    '''
    Create a new note.

    Args:
        note (NoteCreate): Request body containing note details.
        db (Session): Database session dependency.

    Returns:
        NoteResponse: Created note object.

    Raises:
        HTTPException: If user_id is invalid or database error occurs.
    '''
    return create_note(db, note)

@router.get("/{user_id}", response_model=NotesListResponse)
def get(user_id: int, db: Session = Depends(get_db)):
    '''
    Get all notes for a specific user.

    Args:
        user_id (int): ID of the user.
        db (Session): Database session dependency.

    Returns:
        NotesListResponse: Message and list of notes.

    Raises:
        HTTPException: If database error occurs.
    '''
    return get_note(db, user_id)

@router.put("/{note_id}", response_model=NoteResponse)
def update(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    '''
    Update an existing note.

    Args:
        note_id (int): ID of the note to update.
        note (NoteUpdate): Request body with updated fields.
        db (Session): Database session dependency.

    Returns:
        NoteResponse: Updated note object.

    Raises:
        HTTPException: If note is not found or database error occurs.
    '''
    return update_note(db, note_id, note)

@router.delete("/{note_id}")
def delete(note_id: int, db: Session = Depends(get_db)):
    '''
    Delete a note by ID.

    Args:
        note_id (int): ID of the note to delete.
        db (Session): Database session dependency.

    Returns:
        dict: Success message after deletion.

    Raises:
        HTTPException: If note is not found or database error occurs.
    '''
    return delete_note(db, note_id)