# app/schemas/user.py
from pydantic import BaseModel, Field, validator
import re

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    phone: str = Field(..., min_length=10, max_length=10)
    password: str = Field(..., min_length=6, max_length=6)

    @validator("phone")
    def validate_phone(cls, v):
        if not re.fullmatch(r"\d{10}", v):
            raise ValueError("Phone must be a 10-digit number")
        return v

    @validator("password")
    def validate_password(cls, v):
        if not re.fullmatch(r"\d{6}", v):
            raise ValueError("Password must be a 6-digit number only")
        return v

class User(BaseModel):
    id: int
    name: str
    username: str
    phone: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    phone: str = Field(..., min_length=10, max_length=10)
    password: str = Field(..., min_length=6, max_length=6)

    @validator("phone")
    def validate_phone(cls, v):
        if not re.fullmatch(r"\d{10}", v):
            raise ValueError("Phone must be a 10-digit number")
        return v

    @validator("password")
    def validate_password(cls, v):
        if not re.fullmatch(r"\d{6}", v):
            raise ValueError("Password must be a 6-digit number")
        return v

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    id: str
    username: str
    name: str