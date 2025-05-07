from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Post schema for request/response validation
class PostSchema(BaseModel):
    user_id: str
    content: str
    image_url: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
