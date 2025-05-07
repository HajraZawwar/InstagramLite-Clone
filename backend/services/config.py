import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI")

    # AWS
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY")
    USE_DYNAMODB = os.getenv("USE_DYNAMODB", "False") == "True"
