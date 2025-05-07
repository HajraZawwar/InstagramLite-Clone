from datetime import datetime
from bson import ObjectId

# Post Model for MongoDB using PyMongo
class PostDB:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['posts']

    def create_post(self, post_data: dict):
        post = {
            "user_id": post_data['user_id'],
            "content": post_data['content'],
            "image_url": post_data['image_url'],
            "created_at": datetime.utcnow()
        }
        self.collection.insert_one(post)
        return post

    def get_post_by_id(self, post_id: str):
        return self.collection.find_one({"_id": ObjectId(post_id)})

    def get_posts_by_user(self, user_id: str):
        return list(self.collection.find({"user_id": user_id}))

    def update_post(self, post_id: str, update_data: dict):
        return self.collection.update_one({"_id": ObjectId(post_id)}, {"$set": update_data})

    def delete_post(self, post_id: str):
        return self.collection.delete_one({"_id": ObjectId(post_id)})
