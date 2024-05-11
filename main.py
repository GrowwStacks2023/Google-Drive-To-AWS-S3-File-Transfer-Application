from datetime import datetime
from fastapi import FastAPI

from helper__function import uploadToS3
from pydantic import BaseModel

class UploadFile(BaseModel):
    file_url : str

app = FastAPI()

@app.post("/uplaod_to_s3")
async def upload_file_to_s3(upload_file : UploadFile):
    file_id = upload_file.file_url.split("/")[-2]
    response = uploadToS3(file_id)
    
    return {
        "File Id" : file_id,
        "Object Url" : response,
        "Created At" : datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    }