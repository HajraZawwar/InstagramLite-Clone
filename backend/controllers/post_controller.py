from fastapi import APIRouter, HTTPException
from models.post_model import PostDB
from schemas.post_schema import PostSchema
from bson import ObjectId

router = APIRouter()
post_db = PostDB(db) 

@router.post("/create")
async def create_post(post: PostSchema):
    new_post = post_db.create_post(post.dict())
    return new_post

@router.get("/post/{post_id}")
async def get_post(post_id: str):
    post = post_db.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    return post

@router.delete("/delete/{post_id}")
async def delete_post(post_id: str):
    post = post_db.delete_post(post_id)
    if not post.deleted_count:
        raise HTTPException(status_code=404, detail="Post not found.")
    return {"message": "Post deleted successfully."}
