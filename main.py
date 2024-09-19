import os
import gdown
import logging

from connections import connectToAwsS3

logging.basicConfig(level=logging.INFO)

def download_file_from_google_drive(file_id):
    try:
        logging.info(f"Downloading file from Google Drive with ID: {file_id}")
        file_url = f"https://drive.google.com/uc?export=view&id={file_id}"
        file = gdown.download(file_url, quiet=False)
        logging.info(f"File downloaded: {file}")
        return file
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        print(f"An error occurred: {e}")

def uploadToS3(file_id):
    try:
        logging.info(f"Uploading file to S3 with ID: {file_id}")
        file = download_file_from_google_drive(file_id)
        logging.info(f"File downloaded: {file}")

        object_key = os.path.basename(file)
        bucket_name = 'brian01bucket'
        logging.info(f"Connecting to S3 bucket: {bucket_name}")
        s3 = connectToAwsS3()
        logging.info(f"S3 client connected: {s3}")

        logging.info(f"Uploading file to S3: {file} -> {bucket_name}/{object_key}")
        s3.upload_file(file, bucket_name, object_key)
        logging.info(f"File uploaded to S3")

        logging.info(f"Generating presigned URL for S3 object: {bucket_name}/{object_key}")
        response = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_key})
        logging.info(f"Presigned URL generated: {response}")

        logging.info(f"Removing local file: {file}")
        os.remove(file)

        return response
    except Exception as ex:
        logging.error(f"Error uploading file to S3: {ex}")
        print(f"An error occurred: {ex}")
        response = None
        return response
