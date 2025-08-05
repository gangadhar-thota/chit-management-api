from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BidBase(BaseModel):
    chit_id: int
    installment_id: int
    member_id: int
    bid_amount: float = Field(..., ge=0)


class BidCreate(BidBase):
    pass


class BidUpdate(BaseModel):
    bid_amount: Optional[float] = Field(None, ge=0)


class Bid(BidBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
