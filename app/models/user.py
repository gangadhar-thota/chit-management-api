# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
