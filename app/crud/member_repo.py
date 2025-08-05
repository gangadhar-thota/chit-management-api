from sqlalchemy.orm import Session
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate
from typing import List, Optional

class MemberRepository:

    @staticmethod
    def create(db: Session, member_data: MemberCreate, created_by: int) -> Member:
        # Check if phone number already exists for this user
        existing = db.query(Member).filter(
            Member.phone == member_data.phone,
            Member.created_by == created_by,
            Member.is_active == True
        ).first()

        if existing:
            raise ValueError(f"Member with phone {member_data.phone} already exists.")

        new_member = Member(**member_data.dict(), created_by=created_by)
        db.add(new_member)
        db.commit()
        db.refresh(new_member)
        return new_member

    @staticmethod
    def get_by_id(db: Session, member_id: int) -> Optional[Member]:
        return db.query(Member).filter(Member.id == member_id, Member.is_active == True).first()

    @staticmethod
    def get_all(db: Session, created_by: int) -> List[Member]:
        return db.query(Member).filter(Member.created_by == created_by, Member.is_active == True).all()

    @staticmethod
    def update(db: Session, member_id: int, update_data: MemberUpdate, created_by: int) -> Optional[Member]:
        member = db.query(Member).filter(Member.id == member_id, Member.created_by == created_by).first()
        if not member:
            return None
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(member, field, value)
        db.commit()
        db.refresh(member)
        return member

    @staticmethod
    def soft_delete(db: Session, member_id: int, created_by: int) -> bool:
        member = db.query(Member).filter(Member.id == member_id, Member.created_by == created_by).first()
        if not member:
            return False
        member.is_active = False
        db.commit()
        return True

    @staticmethod
    def get_by_ids(db: Session, member_ids: List[str]):
        return db.query(Member).filter(Member.id.in_(member_ids)).all()        

    @staticmethod
    def get_all_by_phone_global(db: Session, phone: str) -> List[Member]:
        return db.query(Member).filter(Member.is_active == True, Member.phone == phone).all()
