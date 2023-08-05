import requests
import pandas as pd

# dados.pe.gov.br/dataset/remuneracao-de-servidores


def get_dataset(url: str) -> pd.DataFrame:
    response = requests.get(url)
    if response.status_code == 200:
        if url.endswith('.json'):
            data = response.json()['campos']
        return pd.DataFrame(data)
    else:
        print('Request to provided URL failed!')
    return None


wages = r'https://dados.pe.gov.br/dataset/7bbfeed7-3019-4c6a-bee7-e1b7411f616b/resource/a0abc7f4-5ea2-408c-8ec1-e0dd8a802fd7/download/2022_12_remuneracao_inativos.json'
df = get_dataset(wages)
print(df.columns)
print(df.describe())
print(df.head())
