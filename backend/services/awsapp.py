from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import uuid

from config import MONGO_URI
from dynamodb_utils import create_user_dynamo, get_user_dynamo, update_user_dynamo, verify_password
from s3_utils import upload_file_to_s3

app = Flask(__name__)
CORS(app)

# MongoDB setup for posts/comments
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["insta_db"]
posts_col = db["posts"]
comments_col = db["comments"]

# ------------------------ User Routes (DynamoDB) ------------------------

@app.route("/signup", methods=["POST"])
def signup():
    data = request.form
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if get_user_dynamo(email):
        return jsonify({"msg": "User already exists"}), 400

    create_user_dynamo(username, email, password)
    return jsonify({"msg": "Signup successful"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.form
    email = data.get("email")
    password = data.get("password")

    user = get_user_dynamo(email)
    if not user or not verify_password(user['password'], password):
        return jsonify({"msg": "Invalid email or password"}), 401

    return jsonify({"msg": "Login successful", "user": user["username"]}), 200

# ------------------------ Post Routes (MongoDB + S3) ------------------------

@app.route("/upload", methods=["POST"])
def upload_post():
    image = request.files.get("image")
    caption = request.form.get("caption")
    email = request.form.get("email")

    if not image or not caption or not email:
        return jsonify({"msg": "Missing fields"}), 400

    image_url = upload_file_to_s3(image)
    post = {
        "_id": str(uuid.uuid4()),
        "email": email,
        "image_url": image_url,
        "caption": caption,
        "likes": [],
        "created_at": datetime.utcnow()
    }
    posts_col.insert_one(post)
    return jsonify({"msg": "Post uploaded", "post": post}), 200


@app.route("/get_posts", methods=["GET"])
def get_posts():
    posts = list(posts_col.find({}, {"_id": 0}))
    return jsonify(posts), 200


@app.route("/like/<post_id>", methods=["PUT"])
def like_post(post_id):
    user_email = request.form.get("email")
    post = posts_col.find_one({"_id": post_id})
    if not post:
        return jsonify({"msg": "Post not found"}), 404

    if user_email in post["likes"]:
        post["likes"].remove(user_email)
    else:
        post["likes"].append(user_email)

    posts_col.update_one({"_id": post_id}, {"$set": {"likes": post["likes"]}})
    return jsonify({"msg": "Like updated"}), 200

# ------------------------ Comment Routes (MongoDB) ------------------------

@app.route("/comment/<post_id>", methods=["POST"])
def add_comment(post_id):
    data = request.form
    comment = {
        "_id": str(uuid.uuid4()),
        "post_id": post_id,
        "email": data.get("email"),
        "text": data.get("text"),
        "created_at": datetime.utcnow()
    }
    comments_col.insert_one(comment)
    return jsonify({"msg": "Comment added"}), 200


@app.route("/comments/<post_id>", methods=["GET"])
def get_comments(post_id):
    comments = list(comments_col.find({"post_id": post_id}, {"_id": 0}))
    return jsonify(comments), 200

# ------------------------ Run ------------------------

if __name__ == "__main__":
    app.run(debug=True)
