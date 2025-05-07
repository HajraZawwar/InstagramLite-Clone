from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# User schema for request/response validation
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    created_at: datetime

    class Config:
        orm_mode = True
