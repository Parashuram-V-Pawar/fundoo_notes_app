from pydantic import BaseModel
from typing import Optional, List


class NoteCreate(BaseModel):
    '''
    Schema for creating a new note.

    Attributes:
        user_id (int): ID of the user who owns the note.
        description (str): Content/description of the note.
    '''
    user_id: int
    description: str


class NoteResponse(BaseModel):
    '''
    Schema for returning a note response.

    Attributes:
        id (int): Unique identifier of the note.
        user_id (int): ID of the user who owns the note.
        description (str): Content of the note.
    '''
    id: int
    user_id: int
    description: str

    class Config:
        from_attributes = True


class NoteUpdate(BaseModel):
    '''
    Schema for updating an existing note.

    Attributes:
        description (Optional[str]): Updated note description.
                                     Optional to allow partial updates.
    '''
    description: Optional[str] = None  


class NotesListResponse(BaseModel):
    '''
    Schema for returning list of notes with a message.

    Attributes:
        message (str): Response message.
        data (List[NoteResponse]): List of notes for the user.
    '''
    message: str
    data: List[NoteResponse]