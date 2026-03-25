from sqlalchemy import Column, Integer, String, Boolean

from config.db import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    password = Column(String(25), nullable=False)
    email = Column(String(254), unique=True, nullable=False, index=True)
    contact_no = Column(String(15))
    is_active = Column(Boolean, default=False)