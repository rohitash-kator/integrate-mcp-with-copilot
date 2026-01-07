"""
Pydantic models for data validation and serialization.
"""

from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class ActivityBase(BaseModel):
    """Base model for Activity."""
    name: str
    description: str
    schedule: str
    max_participants: int
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Chess Club",
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12
            }
        }


class Activity(ActivityBase):
    """Activity model with participants and timestamps."""
    participants: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Chess Club",
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }


class ActivityInDB(Activity):
    """Activity model as stored in database."""
    id: str = Field(alias="_id")
    
    class Config:
        populate_by_name = True


class UserBase(BaseModel):
    """Base model for User."""
    email: EmailStr
    username: str
    role: str = "student"  # student, teacher, admin


class User(UserBase):
    """User model with timestamps."""
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserInDB(UserBase):
    """User model as stored in database."""
    id: str = Field(alias="_id")
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True


class SignupRequest(BaseModel):
    """Request model for signing up a student."""
    email: str
    activity_name: str


class SignupResponse(BaseModel):
    """Response model for signup."""
    message: str
    activity_name: str
    email: str
