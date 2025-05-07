import boto3
import uuid
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME, S3_BUCKET_NAME

s3 = boto3.client(
    's3',
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_file_to_s3(file):
    filename = f"{uuid.uuid4()}_{file.filename}"
    s3.upload_fileobj(file, S3_BUCKET_NAME, filename, ExtraArgs={"ACL": "public-read"})
    return f"https://{S3_BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{filename}"
