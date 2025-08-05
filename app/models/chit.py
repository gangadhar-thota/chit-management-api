from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class Chit(Base):
    __tablename__ = "chits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(15), nullable=False)
    organiser = Column(String(15), nullable=False)
    tenure_type = Column(String(20), nullable=False)
    tenure = Column(Integer, nullable=False)
    amount_per_person = Column(Float, nullable=False)
    commission_per_person = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    bid_date = Column(Date, nullable=False)
    payment_due_date = Column(Date, nullable=False)
    created_by = Column(Integer, nullable=True)
