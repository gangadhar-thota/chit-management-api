from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.chit import Chit
from app.schemas.chit import ChitCreate, ChitUpdate
from app.crud import user_repo
from app.crud.member_repo import MemberRepository

def create_chit(db: Session, chit: ChitCreate, user_id: int):
    db_chit = Chit(**chit.dict())
    db_chit.created_by = user_id
    db.add(db_chit)
    db.commit()
    db.refresh(db_chit)
    return db_chit

def get_all_chits(db: Session, user_id: int):
    return db.query(Chit).filter(Chit.created_by == user_id).all()

def get_chit_by_id(db: Session, chit_id: int, user_id: int):
    return db.query(Chit).filter(Chit.id == chit_id,Chit.created_by == user_id).first()

def update_chit(db: Session, chit_id: int, chit_data: ChitUpdate, user_id: int):
    chit = db.query(Chit).filter(Chit.id == chit_id,Chit.created_by == user_id).first()
    if chit:
        for key, value in chit_data.dict().items():
            setattr(chit, key, value)
        db.commit()
        db.refresh(chit)
    return chit

def delete_chit(db: Session, chit_id: int, user_id: int):
    chit = db.query(Chit).filter(Chit.id == chit_id,Chit.created_by == user_id).first()
    if chit:
        db.delete(chit)
        db.commit()
    return chit

def get_member_chits(db: Session, user_id: int):
    sql = text("""
        SELECT cm.id,cm.member_id, cm.chit_id, cm.invitation_status, cm.created_at as invite_created_at, c.name as chit_name, 
        c.organiser,c.tenure,c.tenure_type,c.amount_per_person,c.commission_per_person,c.start_date,c.bid_date
        FROM users u
        INNER JOIN members m ON u.phone = m.phone
        INNER JOIN chit_members cm ON m.id = cm.member_id
        INNER JOIN chits c ON c.id = cm.chit_id
        WHERE u.id = :user_id
    """)

    result = db.execute(sql, {"user_id": user_id}).mappings().all()
    return list(result)

