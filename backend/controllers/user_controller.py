from fastapi import APIRouter, HTTPException
from models.user_model import UserDB
from schemas.user_schema import UserSchema
from bson import ObjectId

router = APIRouter()

user_db = UserDB(db)  

@router.post("/register")
async def create_user(user: UserSchema):
    existing_user = user_db.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use.")
    new_user = user_db.create_user(user.dict())
    return new_user

@router.get("/user/{user_id}")
async def get_user(user_id: str):
    user = user_db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.put("/update/{user_id}")
async def update_user(user_id: str, user: UserSchema):
    updated_user = user_db.update_user(user_id, user.dict())
    if not updated_user.modified_count:
        raise HTTPException(status_code=404, detail="User not found.")
    return {"message": "User updated successfully."}
