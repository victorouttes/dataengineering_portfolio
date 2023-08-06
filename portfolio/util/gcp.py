from typing import List

import google.cloud.bigquery
import pandas as pd
from google.cloud import storage
from google.cloud import bigquery
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


class BigQuery:
    def __init__(self):
        self.key = '../util/gcp.json'
        self.client = bigquery.Client.from_service_account_json(self.key)

    def create_dataset(self, dataset_name: str):
        dataset_ref = self.client.dataset(dataset_name)
        try:
            self.client.get_dataset(dataset_ref)
            print(f'Dataset {dataset_name} already exists.')
        except Exception as exception:
            dataset = bigquery.Dataset(dataset_ref)
            self.client.create_dataset(dataset)
            print(f'Dataset {dataset_name} created.')
        return dataset_ref

    def load_data(self, table_name: str, dataset: google.cloud.bigquery.DatasetReference, source_path: str):
        table_ref = dataset.table(table_name)
        job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.PARQUET)
        load_job = self.client.load_table_from_uri(
            source_path,
            destination=table_ref,
            job_config=job_config
        )
        load_job.result()
        print(f'Table {table_name} created with data from {source_path}.')

    def query(self, query: str):
        self.client.query(query)
