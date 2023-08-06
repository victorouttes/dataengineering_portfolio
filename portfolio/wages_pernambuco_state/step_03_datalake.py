import pandas as pd

from portfolio.util.gcp import GCP
from portfolio.wages_pernambuco_state import constants


gcloud = GCP()
files = gcloud.list_files(bucket_name=constants.BUCKET_NAME, subfolder=constants.BRONZE_FOLDER)

for file in files:
    print(f'Creating silver layer for file: {file}')
    filename = file.replace(constants.BRONZE_FOLDER, '')
    dataframe = gcloud.read_dataframe(bucket_name=constants.BUCKET_NAME, name=file)
    dataframe.drop([
        'r_total_vantagens',
        'r_imposto_renda',
        'r_outras_vantagens',
        'r_desconto_excedente',
        'r_descontos_compulsorios',
        'r_natalina',
        'r_descontos_previdencia',
        'r_valor_liquido',
        'r_cpf'
    ], axis=1, inplace=True)
    dataframe.rename(columns={
        'r_vencimento_cargo': 'basic_wage',
        'r_categoria': 'category',
        'r_gratificacao_funcao': 'increased_wage_by_function',
        'r_cargo': 'role',
        'r_matricula': 'id',
        'r_nome': 'name',
        'r_outros_creditos': 'extra_wage',
        'r_instituicao': 'locale',
        'r_funcao': 'function',
        'r_remuneracao': 'total_wage',
        'r_ferias': 'vacation_wage',
        'r_descontos_faltas': 'absence_discount'
    }, inplace=True)
    dataframe['absence_discount'] = 0 - dataframe['absence_discount']
    dataframe['updated_at'] = pd.Timestamp.today()
    gcloud.send_dataframe(bucket_name=constants.BUCKET_NAME, name=constants.SILVER_FOLDER + filename, dataframe=dataframe)
