import os
from datetime import datetime, time

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine, storage


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(
        f"File {source_file_name} uploaded to gs://{bucket_name}/{destination_blob_name}."
    )


def upload_blobs(bucket_name, file_to_upload, bucket_path):
    start = datetime.now()
    files_size = 0
    for file_to_upload in files_to_upload:
        source_file_path = os.path.join("./data", file_to_upload)
        files_size += os.path.getsize(source_file_path)
        destination_blob_name = f"{bucket_path}/{file_to_upload}"
        upload_blob(bucket_name, source_file_path, destination_blob_name)
    end = datetime.now()

    files_size = files_size / (1024 * 1024)
    files_size = round(files_size, 2)
    print(
        f"Time taken for uploading the files {len(files_to_upload)} of size {files_size} MB to the bucket: {end - start}")


def import_to_data_store(project_id, data_store_id, location, bucket_name, bucket_path, files_to_upload):
    client_options = (
        ClientOptions(
            api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    client = discoveryengine.DocumentServiceClient(
        client_options=client_options)

    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch="default_branch",
    )

    input_uris = [
        f"gs://{bucket_name}/{bucket_path}/{file}" for file in files_to_upload]

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        gcs_source=discoveryengine.GcsSource(
            input_uris=input_uris,
            data_schema="content",
        ),
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    operation = client.import_documents(request=request)
    print(f"Waiting for operation to complete: {operation.operation.name}")
    response = operation.result()
    metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)
    print(response)
    print(metadata)


project_id = "GDE-Demo"
location = "global"
data_store_id = "test-pdf-data_1740228901592"
bucket_name = "ps-gde-data"
bucket_path = "gde"
files_to_upload = [
    "aak-shea-progress-report-march-20212.pdf",
    "annual-review-2019-en.pdf",
    "6b46f148d2594996b9ba917abc71b14d.pdf",
    "07c3351dcfb300d36fddbb56f7996aea.pdf",
    "063c06110e0fa49b274f044cfef4e92f.pdf",
    "0163af59e5387810eb04c25ff4b03c9d.pdf"
]

upload_blobs(bucket_name, files_to_upload, bucket_path)
import_to_data_store(project_id, data_store_id, location,
                     bucket_name, bucket_path, files_to_upload)
