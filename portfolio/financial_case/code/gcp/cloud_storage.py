from io import BytesIO
from typing import List

import pandas as pd
from google.cloud import storage


class CloudStorage:
    def __init__(self, key: str):
        self.key = key
        self.client = storage.Client.from_service_account_json(self.key)

    def list_files(self, bucket_name: str, sub_folder: str) -> List[str]:
        if not sub_folder.endswith('/'):
            sub_folder += '/'
        try:
            bucket = self.client.get_bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=sub_folder)
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

    def send_dataframe(self, bucket_name: str, folder: str, dataframe: pd.DataFrame) -> bool:
        try:
            today = pd.Timestamp.today()
            filename = folder + today.strftime('%Y%m%d%H%M%S') + '.parquet'

            bucket = self.client.get_bucket(bucket_name)
            buffer = BytesIO()
            dataframe.to_parquet(buffer)
            buffer.seek(0)
            blob = bucket.blob(filename)
            blob.upload_from_file(buffer, content_type='application/octet-stream')
            return True
        except Exception as exception:
            print('Error sending file to bucket!')
            print(exception)
            return False
