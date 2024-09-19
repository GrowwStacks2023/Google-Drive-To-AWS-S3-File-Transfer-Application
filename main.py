import logging
from fastapi import FastAPI, HTTPException
import os
import gdown
from connections import connectToAwsS3

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/download_file_from_google_drive/{file_id}")
async def download_file_from_google_drive(file_id: str):
    try:
        logger.info(f"Downloading file from Google Drive with ID {file_id}")
        file_url = f"https://drive.google.com/uc?export=view&id={file_id}"
        file = gdown.download(file_url, quiet=False)
        logger.info(f"File downloaded successfully: {file}")
        return {"file_path": file}
    except Exception as e:
        logger.error(f"Error occurred while downloading file: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@app.get("/upload_to_s3/{file_id}")
async def upload_to_s3(file_id: str):
    try:
        logger.info(f"Uploading file to S3 with ID {file_id}")
        file = download_file_from_google_drive(file_id)
        logger.info(f"File downloaded from Google Drive: {file}")
        object_key = os.path.basename(file)
        bucket_name = 'brian01bucket'
        logger.info(f"Connecting to S3 bucket {bucket_name}")
        s3 = connectToAwsS3()
        logger.info(f"Uploading file to S3: {file} -> {object_key}")
        s3.upload_file(file, bucket_name, object_key)
        logger.info(f"File uploaded successfully to S3")
        response = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_key})
        logger.info(f"Generated presigned URL: {response}")
        os.remove(file)
        logger.info(f"Removed temporary file: {file}")
        return {"presigned_url": response}
    except Exception as ex:
        logger.error(f"Error occurred while uploading file to S3: {ex}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {ex}")
