from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MemberBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    nickname: Optional[str] = Field(None, max_length=50)
    phone: str = Field(..., min_length=10, max_length=15)
    address: Optional[str] = Field(None, max_length=300)

class MemberCreate(MemberBase):
    pass  # created_by will be set from token in backend, not from client

class MemberUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    nickname: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=15)
    address: Optional[str] = Field(None, max_length=300)
    is_active: Optional[bool] = True

class Member(MemberBase):
    id: int
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
