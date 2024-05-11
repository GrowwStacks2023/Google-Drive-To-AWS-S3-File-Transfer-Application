import os
import gdown

from connections import connectToAwsS3

def download_file_from_google_drive(file_id):
    try:
        # Download the file
        file_url = f"https://drive.google.com/uc?export=view&id={file_id}"
        file = gdown.download(file_url, quiet=False)
        return file
    except Exception as e:
        print(f"An error occurred: {e}")


def uploadToS3(file_id):
    try:        
        file = download_file_from_google_drive(file_id)

        object_key = os.path.basename(file)
        bucket_name = 'brian01bucket'
        s3 = connectToAwsS3()

        s3.upload_file(file, bucket_name, object_key)
        response = s3.generate_presigned_url('get_object',
                                         Params={'Bucket': bucket_name, 'Key': object_key})
        os.remove(file)
    except Exception as ex:
        print(f"An error occurred: {ex}")
        response = None

    return response