from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example="securepassword123")
    contact_consent: bool = Field(default=False, description="Whether user consents to contact")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    two_factor_enabled: Optional[bool] = None
    contact_consent: Optional[bool] = None

class UserInDBBase(UserBase):
    id: UUID
    role: UserRole = UserRole.USER
    two_factor_enabled: bool = False
    two_factor_verified: bool = False
    contact_consent: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {UUID: str}

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password_hash: str
