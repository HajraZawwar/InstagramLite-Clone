import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

s3 = boto3.client('s3')

def upload_file_to_s3(file, bucket_name: str, file_name: str):
    try:
        s3.upload_fileobj(file, bucket_name, file_name)
        return f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    except (NoCredentialsError, PartialCredentialsError) as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "An error occurred while uploading the file."}
