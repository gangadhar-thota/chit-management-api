from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.password import hash_password, verify_password
from typing import List

def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()

def create_user(db: Session, user: UserCreate):
    username = user.name.strip().lower().replace(" ", "_")
    db_user = User(
        name=user.name,
        username=username,
        phone=user.phone,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, phone: str, password: str):
    user = db.query(User).filter(User.phone == phone).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()    

def get_users_by_phones(db: Session, phones: List[str]):
    return db.query(User).filter(User.phone.in_(phones)).all()