from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import boto3
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB
mongo_uri = os.getenv('MONGO_URI')
mongo_client = MongoClient(mongo_uri)
db = mongo_client['InstagramLiteCluster']  
users_collection = db['users']
posts_collection = db['posts']

# AWS S3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('S3_REGION')
)
bucket_name = os.getenv('S3_BUCKET_NAME')

# FastAPI setup
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Pydantic models for input validation
class User(BaseModel):
    email: str
    password: str

class Post(BaseModel):
    user_id: str
    caption: str

class UpdateProfile(BaseModel):
    user_id: str
    username: str = None
    full_name: str = None
    bio: str = None
    profile_picture_url: str = None

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/register")
async def register(user: User):
    hashed_password = bcrypt.generate_password_hash(user.password).decode('utf-8')
    user_id = str(uuid4())
    user_data = {
        "_id": user_id,
        "email": user.email,
        "password": hashed_password
    }
    users_collection.insert_one(user_data)
    return {"message": "User registered successfully!"}

@app.post("/login")
async def login(user: User):
    user_data = users_collection.find_one({"email": user.email})
    if user_data and bcrypt.check_password_hash(user_data['password'], user.password):
        return {"message": "Login Successful", "user_id": str(user_data['_id'])}
    else:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

@app.post("/upload")
async def upload_post(file: UploadFile = File(...), caption: str = None, user_id: str = None):
    if not file:
        raise HTTPException(status_code=400, detail="No file part")
    if file.filename == '':
        raise HTTPException(status_code=400, detail="No selected file")
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type")

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, 'wb') as buffer:
        buffer.write(await file.read())

    post_data = {
        "_id": str(uuid4()),
        "user_id": user_id,
        "caption": caption,
        "media_url": file_path,
        "created_at": datetime.utcnow(),
        "likes": 0,
        "comments": []
    }
    posts_collection.insert_one(post_data)
    return {"message": "Post uploaded successfully!"}

@app.get("/feed")
async def get_feed():
    posts = list(posts_collection.find({}).sort("created_at", -1))
    for post in posts:
        post['_id'] = str(post['_id'])
        post['media_url'] = f"/static/uploads/{os.path.basename(post['media_url'])}"
    return JSONResponse(content=jsonable_encoder(posts))

@app.get("/get_user/{user_id}")
async def get_user(user_id: str):
    user = users_collection.find_one({"_id": user_id})
    if user:
        user['_id'] = str(user['_id'])
        user.pop('password', None)  # Remove password
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/update_profile")
async def update_profile(profile: UpdateProfile):
    update_data = {k: v for k, v in profile.dict().items() if v is not None}
    result = users_collection.update_one({"_id": profile.user_id}, {"$set": update_data})
    if result.modified_count > 0:
        return {"message": "Profile updated successfully!"}
    else:
        raise HTTPException(status_code=404, detail="User not found or no changes applied")

@app.post("/add_comment")
async def add_comment(post_id: str, user_id: str, text: str):
    if not post_id or not user_id or not text:
        raise HTTPException(status_code=400, detail="Missing required fields")

    comment = {
        "user_id": user_id,
        "text": text,
        "timestamp": datetime.utcnow()
    }
    result = posts_collection.update_one(
        {"_id": post_id},
        {"$push": {"comments": comment}}
    )

    if result.modified_count > 0:
        return {"message": "Comment added successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")

@app.get("/")
async def read_root():
    return {"message": "SnapConnect API is running."}
