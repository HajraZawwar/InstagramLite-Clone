from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId

# Define User model as Pydantic Schema for validation
class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True


# User Model for MongoDB using PyMongo
class UserDB:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['users']

    def create_user(self, user_data: dict):
        user = {
            "username": user_data['username'],
            "email": user_data['email'],
            "password": user_data['password'],
            "created_at": datetime.utcnow()
        }
        self.collection.insert_one(user)
        return user

    def get_user_by_email(self, email: str):
        return self.collection.find_one({"email": email})

    def get_user_by_id(self, user_id: str):
        return self.collection.find_one({"_id": ObjectId(user_id)})

    def update_user(self, user_id: str, update_data: dict):
        return self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

    def delete_user(self, user_id: str):
        return self.collection.delete_one({"_id": ObjectId(user_id)})
