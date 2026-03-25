from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Dict, List

from src.models.users import User
from src.schema.users_schema import *
from config.logger import logger


def create_user(db: Session, user: UserCreate) -> User:
    '''
    Creates a new user in the database.
    
    Args:
        db (Session): Database session for performing operations.
        user (UserCreate): Pydantic model containing user details.
        
    Returns:
        User: The created user object.
    Raises:
        HTTPException: If there's an integrity error or database error.
    '''

    try:
        logger.info("Creating user")

        new_user = User(**user.model_dump())

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.bind(user_id=new_user.id, email=new_user.email).info(
            "User created successfully"
        )
        return new_user

    except IntegrityError:
        db.rollback()
        logger.bind(email=user.email).error("Integrity error creating user")
        raise HTTPException(status_code=400, detail="User with given email already exists")

    except SQLAlchemyError:
        db.rollback()
        logger.bind(email=user.email).error("Database error creating user")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_users(db: Session) -> List[User]:
    '''
    Fetches all users from the database.
    Args:
        db (Session): Database session for performing operations.
           
    Returns:
        list[User]: A list of user objects.
    Raises:
        HTTPException: If there's a database error.
    '''

    try:
        logger.info("Fetching all users")
        return db.query(User).all()

    except SQLAlchemyError:
        logger.error("Error fetching users")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_user(db: Session, user_id: int) -> User:
    '''
    Fetches a user by their ID from the database.
    
    Args:
        db (Session): Database session for performing operations.
        user_id (int): The ID of the user to fetch.
        
    Returns:
        User: The fetched user object.
    Raises:
        HTTPException: If the user is not found or there's a database error.
    '''

    try:
        logger.bind(user_id=user_id).info("Fetching user")

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.bind(user_id=user_id).warning("User not found")
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except SQLAlchemyError:
        logger.bind(user_id=user_id).error("Database error fetching user")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def update_user(db: Session, user_id: int, current_user: UserUpdate) -> User:
    try:
        logger.info(f"Updating user {user_id}")
        
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # update fields
        user.name = current_user.name
        user.email = current_user.email
        user.contact_no = current_user.contact_no
        user.is_active = current_user.is_active
        user.password = current_user.password

        db.commit()
        db.refresh(user)

        return user

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

def delete_user(db: Session, user_id: int) -> Dict:
    '''
    Deletes a user from the database.
    
    Args:
        db (Session): Database session for performing operations.
        user_id (int): The ID of the user to delete.
        
    Returns:
        Dict: A dictionary containing a success message.
    Raises:
        HTTPException: If the user is not found or there's a database error.
    '''

    try:
        logger.info(f"Deleting user: {user_id}")

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.bind(user_id=user_id).warning("User not found")
            raise HTTPException(status_code=404, detail="User Not Found")

        db.delete(user)
        db.commit()

        logger.bind(user_id=user_id).info("User deleted successfully")
        return {"message": f"User {user_id} deleted successfully"}

    except IntegrityError:
        db.rollback()
        logger.bind(user_id=user_id).error("Integrity error deleting user")
        raise HTTPException(
            status_code=400,
            detail="Cannot delete user: linked records exist"
        )

    except SQLAlchemyError:
        db.rollback()
        logger.bind(user_id=user_id).error("Database error deleting user")
        raise HTTPException(status_code=500, detail="Internal Server Error")