import pandas as pd
import requests
from bs4 import BeautifulSoup

from portfolio.util.gcp import GCP
from portfolio.wages_pernambuco_state import constants


def get_dataset(url: str) -> pd.DataFrame:
    response = requests.get(url)
    if response.status_code == 200:
        if url.endswith('.json'):
            data = response.json()['campos']
        return pd.DataFrame(data)
    else:
        print('Request to provided URL failed!')
    return None


def scrape_links_from_source() -> dict:
    response = requests.get(constants.INGESTION_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    file_pattern = '2022_{:02d}_remuneracao_ativos.json'
    links = {}
    for month in range(1, 13):
        pattern = file_pattern.format(month)
        for link in soup.find_all('a', href=True):
            if pattern in link['href']:
                links[month] = link['href']
    return links


gcloud = GCP()
files_to_download = scrape_links_from_source()
for month in files_to_download.keys():
    print(f'Collecting data from month: {month}')
    dataframe = get_dataset(files_to_download[month])
    filename = '2022/{:02d}/'.format(month) + pd.Timestamp.today().strftime('%Y%m%d%H%M%S') + '.parquet'
    gcloud.send_dataframe(bucket_name=constants.BUCKET_NAME, name=constants.BRONZE_FOLDER + filename, dataframe=dataframe)
