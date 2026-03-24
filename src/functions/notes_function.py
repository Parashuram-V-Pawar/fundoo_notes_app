from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.config.logger import logger
from src.models.notes import Note
from src.schema.notes_schema import *

def create_note(db: Session, note: NoteCreate) -> Note:
    '''
    Creates a new note in the database.

    Args:
        db (Session): Database session for performing operations.
        note (NoteCreate): Pydantic model containing note details.

    Returns:
        Note: The created note object.

    Raises:
        HTTPException: If user_id is invalid or database error occurs.
    '''
    try:
        logger.info("Creating note")

        new_note = Note(**note.model_dump())
        
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        
        logger.bind(
            note_id=new_note.id,
            user_id=new_note.user_id
        ).info("Note created successfully")
        
        return new_note
    
    except IntegrityError:
        db.rollback()
        
        logger.bind(
            user_id=note.user_id
        ).error("Integrity error creating note")
        
        raise HTTPException(
            status_code=400,
            detail="Invalid user_id"
        )
    
    except SQLAlchemyError:
        db.rollback()
        
        logger.bind(
            user_id=note.user_id
        ).exception("Database error creating note")
        
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
def get_note(db: Session, user_id: int):
    '''
    Fetches all notes for a given user.

    Args:
        db (Session): Database session for performing operations.
        user_id (int): ID of the user.

    Returns:
        dict: Message and list of notes (can be empty).

    Raises:
        HTTPException: If a database error occurs.
    '''
    try:
        logger.bind(user_id=user_id).info("Fetching all notes")

        notes = db.query(Note).filter(Note.user_id == user_id).all()

        # 🧠 Handle empty notes case
        if not notes:
            logger.bind(user_id=user_id).warning(
                "No notes found for the given user id"
            )
            return {
                "message": "No notes found for this user",
                "data": []
            }

        logger.bind(user_id=user_id).info("Notes fetched successfully")
        return {
            "message": "Notes fetched successfully",
            "data": notes
        }
    
    except SQLAlchemyError:
        logger.bind(user_id=user_id).error("Database error while fetching notes")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    
    except SQLAlchemyError:
        logger.bind(user_id=user_id).error(
            "Database error fetching notes"
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
   
def update_note(db: Session, note_id: int, req: NoteUpdate) -> Note:
    '''
    Updates an existing note in the database.

    Args:
        db (Session): Database session for performing operations.
        note_id (int): ID of the note to update.
        req (NoteUpdate): Pydantic model containing updated note data.

    Returns:
        Note: The updated note object.

    Raises:
        HTTPException: If note is not found or database error occurs.
    '''
    try:
        note = db.query(Note).filter(Note.id == note_id).first()

        if not note:
            raise HTTPException(status_code=404, detail="Note not found")

        if req.description is not None:
            note.description = req.description

        db.commit()
        db.refresh(note)

        return note

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
def delete_note(db: Session, note_id: int) -> dict:
    '''
    Deletes a note from the database.

    Args:
        db (Session): Database session for performing operations.
        note_id (int): ID of the note to delete.

    Returns:
        dict: Success message after deletion.

    Raises:
        HTTPException: If note is not found, integrity issue, or database error occurs.
    '''
    try:
        logger.bind(note_id = note_id).info("Deleting note")
        
        note = db.query(Note).filter(Note.id == note_id).first()
        
        if not note:
            logger.bind(note_id = note_id).warning(
                "Note not found"
            )
            raise HTTPException(
                status_code=404,
                detail="Note not found"
            )
        
        db.delete(note)
        db.commit()
        
        logger.bind(note_id = note_id).info("Note deleted successfully")
        return {"message": f"Note {note_id} deleted successfully"}
    
    except IntegrityError as e:
        db.rollback()
        logger.bind(note_id = note_id).error(
            "Integrity error deleting note"
        )
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete note: linked records exist"
        )
        
    except SQLAlchemyError as e:
        logger.bind(note_id = note_id).error(
            "Database error deleting note"
        )
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")