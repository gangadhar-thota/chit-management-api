from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, DateTime, func, String
from app.database import Base

class ChitMember(Base):
    __tablename__ = "chit_members"

    id = Column(Integer, primary_key=True, index=True)
    chit_id = Column(Integer, nullable=False)
    member_id = Column(Integer, nullable=False)
    invitation_status = Column(String(15), nullable=False, default="Pending")  # 0: Pending, 1: Accepted, 2: Rejected
    amount_paid = Column(Float, default=0)
    amount_due = Column(Float, default=0)
    is_taken = Column(Boolean, default=False)
    bid_amount = Column(Float, default=0)
    taken_amount = Column(Float, default=0)
    taken_installment = Column(Integer, default=0)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
