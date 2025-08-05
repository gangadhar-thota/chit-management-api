from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime

class ChitMemberBase(BaseModel):
    chit_id: int
    member_id: int

class ChitMemberCreate(ChitMemberBase):
    pass

class ChitMember(ChitMemberBase):
    id: int
    invitation_status: str
    amount_paid: float
    amount_due: float
    is_taken: bool
    bid_amount: float
    taken_amount: float
    taken_installment: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class InvitationStatusEnum(str, Enum):
    accepted = "accepted"
    rejected = "rejected"

class UpdateInvitationStatusRequest(BaseModel):
    id: int = Field(..., gt=0)
    status: InvitationStatusEnum
