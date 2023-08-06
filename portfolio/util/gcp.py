from typing import List

import pandas as pd
from google.cloud import storage
from io import BytesIO


class GCP:
    def __init__(self):
        self.key = '../util/gcp.json'
        self.client = storage.Client.from_service_account_json(self.key)

    def list_files(self, bucket_name: str, subfolder: str) -> List[str]:
        if not subfolder.endswith('/'):
            subfolder += '/'
        try:
            bucket = self.client.get_bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=subfolder)
            return [blob.name for blob in blobs]
        except Exception as exception:
            print('Error reading files from bucket!')
            print(exception)
            return []

    def read_dataframe(self, bucket_name: str, name: str) -> pd.DataFrame:
        try:
            bucket = self.client.get_bucket(bucket_name)
            blob = bucket.blob(name)
            buffer = BytesIO()
            blob.download_to_file(buffer)
            buffer.seek(0)
            return pd.read_parquet(buffer)
        except Exception as exception:
            print('Error reading file from bucket!')
            print(exception)
            return None

    def send_dataframe(self, bucket_name: str, name: str, dataframe: pd.DataFrame) -> bool:
        try:
            bucket = self.client.get_bucket(bucket_name)
            buffer = BytesIO()
            dataframe.to_parquet(buffer)
            buffer.seek(0)
            blob = bucket.blob(name)
            blob.upload_from_file(buffer, content_type='application/octet-stream')
            return True
        except Exception as exception:
            print('Error sending file to bucket!')
            print(exception)
            return False
