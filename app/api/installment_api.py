from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from app.utils.auth_router import get_authenticated_router
from app.schemas.installment import InstallmentCreate, Installment, InstallmentUpdate
from app.crud import installment_repo

router = get_authenticated_router(prefix="/installments", tags=["Installments"])

@router.post("/add", response_model=Installment)
def create(data: InstallmentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return installment_repo.create_installment(db, data, user.id)

@router.get("/", response_model=list[Installment])
def get_all(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return installment_repo.get_all(db, user.id)

@router.get("/{installment_id}", response_model=Installment)
def get_by_id(installment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    result = installment_repo.get_by_id(db, installment_id, user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Installment not found")
    return result

@router.put("/update/{installment_id}", response_model=Installment)
def update(installment_id: int, data: InstallmentUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    result = installment_repo.update_installment(db, installment_id, data, user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Installment not found or not owned by you")
    return result
