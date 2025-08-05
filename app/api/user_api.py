from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, User, Token, UserLogin
from app.crud import user_repo
from app.database import get_db
from app.utils.auth import create_access_token

router = APIRouter()

@router.post("/signup", response_model=User)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_repo.get_user_by_phone(db, user.phone)
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone already registered")
    
    return user_repo.create_user(db, user)

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    auth_user = user_repo.authenticate_user(db, user.phone, user.password)
    if not auth_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid phone or password")

    token = create_access_token(
        data={
            "sub": str(auth_user.id),
            "name": auth_user.name,
            "username": auth_user.username,
            "phone": auth_user.phone
            }
        )
    return {"access_token": token, "token_type": "bearer"}