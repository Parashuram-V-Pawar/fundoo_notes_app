from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.utils.db_dependency import get_db
from src.schema.users_schema import *
from src.functions.users_function import *

router = APIRouter(prefix="/users", tags=["Users"])

@router.post('/', response_model=UserResponse)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/all", response_model=list[UserResponse])
def all_users(db: Session = Depends(get_db)):
    return get_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def search(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)

@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
