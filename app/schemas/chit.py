from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ChitBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=15)
    organiser: str = Field(..., min_length=3, max_length=15)
    tenure_type: str
    tenure: int 
    amount_per_person: float
    commission_per_person: float
    start_date: date
    bid_date: date
    payment_due_date: date

class ChitCreate(ChitBase):
    pass

class ChitUpdate(ChitBase):
    pass

class Chit(ChitBase):
    id: int
    created_by: Optional[int]

    class Config:
        orm_mode = True
