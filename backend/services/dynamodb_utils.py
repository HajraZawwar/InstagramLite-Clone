import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME
from flask_bcrypt import Bcrypt

dynamodb = boto3.resource(
    'dynamodb',
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

bcrypt = Bcrypt()

users_table = dynamodb.Table("Users")

def create_user_dynamo(username, email, password):
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    users_table.put_item(
        Item={
            "email": email,
            "username": username,
            "password": hashed_pw
        }
    )
    return True

def get_user_dynamo(email):
    response = users_table.get_item(Key={"email": email})
    return response.get("Item")

def update_user_dynamo(email, data):
    update_expr = "SET " + ", ".join(f"{k}=:{k}" for k in data)
    expr_values = {f":{k}": v for k, v in data.items()}
    users_table.update_item(
        Key={"email": email},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_values
    )
    return True

def verify_password(stored_hash, input_password):
    return bcrypt.check_password_hash(stored_hash, input_password)
