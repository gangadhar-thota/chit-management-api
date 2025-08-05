from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from app.utils.auth_router import get_authenticated_router

from app.schemas.chit_member import ChitMember, ChitMemberCreate, UpdateInvitationStatusRequest
from app.crud import chit_member_repo, user_repo
from app.crud.member_repo import MemberRepository

router = get_authenticated_router(prefix="/chit_members", tags=["Chit Members"])

@router.post("/add", response_model=ChitMember)
def add_member(
    payload: ChitMemberCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return chit_member_repo.add_member_to_chit(db, payload, current_user.id)

@router.delete("/delete")
def remove_member(
    chit_id: int,
    member_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return chit_member_repo.delete_member_from_chit(db, chit_id, member_id, current_user.id)

@router.get("/list")
def list_members(
    chit_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    chit_members = chit_member_repo.get_members_by_chit(db, chit_id, current_user.id)
    member_details = MemberRepository.get_by_ids(db, [cm.member_id for cm in chit_members])
    response = []
    for member in member_details:
        chit_member = next((cm for cm in chit_members if cm.member_id == member.id), None)
        if chit_member:
            response.append({
                "id": chit_member.id,
                "chit_id": chit_member.chit_id,
                "member_id": member.id,
                "invitation_status": chit_member.invitation_status,
                "amount_paid": chit_member.amount_paid,
                "amount_due": chit_member.amount_due,
                "is_taken": chit_member.is_taken,
                "bid_amount": chit_member.bid_amount,
                "taken_amount": chit_member.taken_amount,
                "taken_installment": chit_member.taken_installment,
                "created_by": chit_member.created_by,
                "created_at": chit_member.created_at,
                "updated_at": chit_member.updated_at,
                "name": member.name,  # Assuming Member model has a 'name' field
                "phone": member.phone  # Assuming Member model has a 'phone' field
            })

    return response

@router.put("/invitation-status")
def update_invitation_status(
    payload: UpdateInvitationStatusRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # optional
):
    updated = chit_member_repo.update_invitation_status(
        db=db,
        chit_member_id=payload.id,
        status=payload.status,
    )
    return {"message": "Invitation status updated", "data": updated}
    
