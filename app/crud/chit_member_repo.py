from sqlalchemy.orm import Session
from app.models.chit_member import ChitMember
from app.schemas.chit_member import ChitMemberCreate

def add_member_to_chit(db: Session, data: ChitMemberCreate, user_id: int):
     # Check if member is already in chit
    existing = db.query(ChitMember).filter_by(
        chit_id=data.chit_id,
        member_id=data.member_id,
        created_by=user_id
    ).first()

    if existing:
        raise ValueError("Member is already part of this chit")
    
    db_entry = ChitMember(
        **data.dict(),
        amount_paid=0,
        amount_due=0,
        is_taken=False,
        bid_amount=0,
        taken_amount=0,
        taken_installment=0,
        created_by=user_id
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def delete_member_from_chit(db: Session, chit_id: int, member_id: int, user_id: int):
    entry = db.query(ChitMember).filter_by(chit_id=chit_id, member_id=member_id, created_by=user_id).first()
    if entry:
        db.delete(entry)
        db.commit()
    return entry

def get_members_by_chit(db: Session, chit_id: int, user_id: int):
    return db.query(ChitMember).filter_by(chit_id=chit_id, created_by=user_id).all()

def update_invitation_status(db: Session, chit_member_id: int, status: str):
    chit_member = db.query(ChitMember).filter(ChitMember.id == chit_member_id).first()

    if not chit_member:
        raise HTTPException(status_code=404, detail="Chit member not found")

    chit_member.invitation_status = status
    db.commit()
    db.refresh(chit_member)

    return chit_member
