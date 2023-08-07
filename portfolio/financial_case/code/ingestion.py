import pandas as pd

from gcp.cloud_storage import CloudStorage
from gcp.constants import BUCKET_NAME, BRONZE_FOLDER, CSV_FOLDER


def run():
    print(f'Sending raw data to {BUCKET_NAME}...')

    storage = CloudStorage(key='../keys/gcp_victorouttes_portfolio_service_account_key.json')
    storage.send_dataframe(bucket_name=BUCKET_NAME, folder=BRONZE_FOLDER+'pix/', dataframe=pd.read_csv(CSV_FOLDER + 'pix_movements/pix.csv'))
    storage.send_dataframe(bucket_name=BUCKET_NAME, folder=BRONZE_FOLDER+'transfer_ins/', dataframe=pd.read_csv(CSV_FOLDER + 'transfer_ins/transfer_ins.csv'))
    storage.send_dataframe(bucket_name=BUCKET_NAME, folder=BRONZE_FOLDER+'transfer_outs/', dataframe=pd.read_csv(CSV_FOLDER + 'transfer_outs/transfer_outs.csv'))
    storage.send_dataframe(bucket_name=BUCKET_NAME, folder=BRONZE_FOLDER+'accounts/', dataframe=pd.read_csv(CSV_FOLDER + 'accounts/accounts.csv'))
    storage.send_dataframe(bucket_name=BUCKET_NAME, folder=BRONZE_FOLDER+'customers/', dataframe=pd.read_csv(CSV_FOLDER + 'customers/customers.csv'))
