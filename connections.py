import os
import boto3
from dotenv import load_dotenv


def connectToAwsS3():
    load_dotenv()
    s3 = boto3.client(
    's3',
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name = os.getenv("REGION_NAME")
    )
    return s3


if __name__ == "__main__":
    load_dotenv()
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name = os.getenv("REGION_NAME")

    print(aws_access_key_id[0], aws_secret_access_key[0], region_name)