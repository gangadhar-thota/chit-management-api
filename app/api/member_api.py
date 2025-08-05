from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from app.utils.auth_router import get_authenticated_router

from app.schemas.member import Member, MemberCreate, MemberUpdate
from app.crud.member_repo import MemberRepository
from app.crud.user_repo import get_users_by_phones

router = get_authenticated_router(prefix="/members", tags=["Members"])

@router.post("/add", response_model=Member)
def create_member(
    member: MemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
   try:
        return MemberRepository.create(db, member, current_user.id)
   except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))        


@router.get("/list")
def get_all_members(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    members = MemberRepository.get_all(db, current_user.id)
    users = get_users_by_phones(db, [m.phone for m in members])
    registered_phones = {u.phone for u in users}

    response = []
    for m in members:
        response.append({
            "id": m.id,
            "name": m.name,
            "nickname": m.nickname,
            "phone": m.phone,
            "address": m.address,
            "is_active": m.is_active,
            "created_by": m.created_by,
            "created_at": m.created_at,
            "updated_at": m.updated_at,
            "is_registered": m.phone in registered_phones
        })
    return response    


@router.get("/{member_id}", response_model=Member)
def get_member_by_id(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    member = MemberRepository.get_by_id(db, member_id, current_user.id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.put("/update/{member_id}", response_model=Member)
def update_member(
    member_id: int,
    member: MemberUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    updated_member = MemberRepository.update(db, member_id, member, current_user.id)
    if not updated_member:
        raise HTTPException(status_code=404, detail="Member not found or unauthorized")
    return updated_member


@router.delete("/delete/{member_id}")
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    success = MemberRepository.soft_delete(db, member_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found or unauthorized")
    return {"success": True, "message": "Member deactivated"}    
