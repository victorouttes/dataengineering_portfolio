from portfolio.util.gcp import BigQuery
from portfolio.wages_pernambuco_state import constants

bquery = BigQuery()
dataset = bquery.create_dataset('portfolio_pernambuco_wages')
bquery.load_data(
    table_name='wages_2022',
    dataset=dataset,
    source_path=f'gs://{constants.BUCKET_NAME}/{constants.SILVER_FOLDER}*.parquet'
)
