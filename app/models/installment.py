from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, DECIMAL
from sqlalchemy.sql import func
from app.database import Base

class Installment(Base):
    __tablename__ = "installments"

    id = Column(Integer, primary_key=True, index=True)
    chit_id = Column(Integer, nullable=False)
    installment_no = Column(Integer, nullable=False)
    bid_amount = Column(DECIMAL(10, 2), default=0)
    winner_id = Column(Integer, nullable=True)
    is_settled = Column(Boolean, default=False)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
