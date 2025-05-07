from config import Config

def test_config():
    assert Config.MONGO_URI is not None, "MONGO_URI is not set"
    assert Config.AWS_ACCESS_KEY_ID is not None, "AWS_ACCESS_KEY_ID is not set"
    assert Config.AWS_SECRET_ACCESS_KEY is not None, "AWS_SECRET_ACCESS_KEY is not set"
    assert Config.AWS_REGION is not None, "AWS_REGION is not set"
    assert Config.S3_BUCKET_NAME is not None, "S3_BUCKET_NAME is not set"
    assert Config.SECRET_KEY is not None, "SECRET_KEY is not set"
    print("All configuration variables are set.")