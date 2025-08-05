from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.chit import Chit, ChitCreate, ChitUpdate
from app.crud import chit_repo
from app.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from app.utils.auth_router import get_authenticated_router

router = get_authenticated_router(prefix="/chits", tags=["Chits"])

@router.post("/", response_model=Chit)
def create_chit(chit: ChitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return chit_repo.create_chit(db, chit, user_id=current_user.id)

@router.get("/", response_model=List[Chit])
def list_chits(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return chit_repo.get_all_chits(db, user_id=current_user.id)

@router.get("/{chit_id}", response_model=Chit)
def get_chit(chit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chit = chit_repo.get_chit_by_id(db, chit_id, user_id=current_user.id)
    if not chit:
        raise HTTPException(status_code=404, detail="Chit not found")
    return chit

@router.put("/{chit_id}", response_model=Chit)
def update_chit(chit_id: int, chit_data: ChitUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chit = chit_repo.update_chit(db, chit_id, chit_data, user_id=current_user.id)
    if not chit:
        raise HTTPException(status_code=404, detail="Chit not found")
    return chit

@router.delete("/{chit_id}")
def delete_chit(chit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chit = chit_repo.delete_chit(db, chit_id, user_id=current_user.id)
    if not chit:
        raise HTTPException(status_code=404, detail="Chit not found")
    return {"message": "Chit deleted"}

@router.get("/member/all")
def list_chits(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return chit_repo.get_member_chits(db, user_id=current_user.id)