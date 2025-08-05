from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InstallmentBase(BaseModel):
    chit_id: int
    installment_no: int
    bid_amount: float = 0
    winner_id: Optional[int] = None
    is_settled: bool = False

class InstallmentCreate(InstallmentBase):
    pass

class InstallmentUpdate(BaseModel):
    bid_amount: Optional[float] = None
    winner_id: Optional[int] = None
    is_settled: Optional[bool] = None

class Installment(InstallmentBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
