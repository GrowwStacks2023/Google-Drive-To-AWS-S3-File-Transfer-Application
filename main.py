from datetime import datetime
from fastapi import FastAPI

from helper__function import uploadToS3
from pydantic import BaseModel

class UploadFile(BaseModel):
    file_id : str

app = FastAPI()

@app.post("/uplaod_to_s3")
async def upload_file_to_s3(upload_file : UploadFile):
    response = uploadToS3(upload_file.file_id)

    return {
        "File Id" : upload_file.file_id,
        "Object Url" : response,
        "Created At" : datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    }
