import os
from datetime import datetime, time

from google.cloud import storage


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(
        f"File {source_file_name} uploaded to gs://{bucket_name}/{destination_blob_name}."
    )


def upload_blobs(bucket_name, file_to_upload, destination_folder_name):
    start = datetime.now()
    files_size = 0
    for file_to_upload in files_to_upload:
        source_file_path = os.path.join("./data", file_to_upload)
        files_size += os.path.getsize(source_file_path)
        destination_blob_name = f"{destination_folder_name}/{file_to_upload}"
        upload_blob(bucket_name, source_file_path, destination_blob_name)
    end = datetime.now()

    files_size = files_size / (1024 * 1024)
    files_size = round(files_size, 2)
    print(
        f"Time taken for uploading the files {len(files_to_upload)} of size {files_size} MB to the bucket: {end - start}")


bucket_name = "ps-gde-data"  # Replace with your bucket name
files_to_upload = [
    "aak-shea-progress-report-march-20212.pdf",
    "annual-review-2019-en.pdf",
    "6b46f148d2594996b9ba917abc71b14d.pdf",
    "07c3351dcfb300d36fddbb56f7996aea.pdf",
    "063c06110e0fa49b274f044cfef4e92f.pdf",
    "0163af59e5387810eb04c25ff4b03c9d.pdf"
]
destination_folder_name = "gde"
upload_blobs(bucket_name, files_to_upload, destination_folder_name)
