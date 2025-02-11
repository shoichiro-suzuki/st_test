# pip install azure-storage-blob
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

# ストレージアカウント接続文字列
load_dotenv()
connection_string = os.getenv("BLOB_STORAGE_CONNECTION_STRING")


def upload_blob_to_azure(container_name, blob_name, data):
    # BlobServiceClient のインスタンスを作成
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # コンテナクライアントを取得
    container_client = blob_service_client.get_container_client(container_name)

    # Blobをアップロード
    try:
        container_client.upload_blob(name=blob_name, data=data)
        message = f"{blob_name} has been uploaded to {container_name} container."
        print(message)
    except Exception as e:
        message = f"Failed to upload {blob_name} to {container_name} container."
        print(message)
        print(e)

    return message
