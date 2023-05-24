from azure.storage.blob import BlobClient
from scrapy.utils.project import get_project_settings

def save(response):
    settings=get_project_settings()
    conn_str = settings.get("AZURE_BLOB_CONNECTION_STRING")
    container_name=settings.get("AZURE_BLOB_CONTAINER_NAME")
    blob_name=response.url.split("/")[-1] + '.html'
    blob = BlobClient.from_connection_string(conn_str, container_name, blob_name)
    blob.upload_blob(data=response.body)