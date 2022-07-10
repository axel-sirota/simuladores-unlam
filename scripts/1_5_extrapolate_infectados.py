import os

import pandas as pd

DATA_FOLDER = f'{os.getcwd()}/data'
INFECTADOS_PATH = f'{DATA_FOLDER}/infectados.csv'
INFECTADOS_EXTRAPOLADO_PATH = f'{DATA_FOLDER}/infectados_extrapolado.csv'
MONTHS = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGOS', 'SEP', 'OCT', 'NOV', 'DIC']
pd.set_option('display.max_columns', None)
try:
    infectados_no_extrapolado = pd.read_csv(INFECTADOS_PATH)
except FileNotFoundError as e:
    print(f'Please run notebook/script 1_process_raw_data')
    raise e

infectados_no_extrapolado['DIC'] = infectados_no_extrapolado['DIC'] + infectados_no_extrapolado['otros']
infectados_no_extrapolado.drop(columns=['otros'], inplace=True)
print(infectados_no_extrapolado)
year_index = infectados_no_extrapolado.ANO.copy(deep=True)
df = pd.DataFrame(columns=MONTHS, index=infectados_no_extrapolado.index)

for index, row in df.iterrows():
    for index_col, month in enumerate(MONTHS):
        if index == 0 and index_col == 0:
            df[month][index] = infectados_no_extrapolado.reset_index(drop=True)[month][index]
        elif index_col == 0:
            df['ENE'][index] = df['DIC'][index-1] + infectados_no_extrapolado['ENE'][index]
        elif index_col > 0:
            df[month][index] = df[MONTHS[index_col-1]][index] + infectados_no_extrapolado.reset_index(drop=True)[month][index]
df.set_index(year_index, inplace=True)
# df.to_csv(INFECTADOS_EXTRAPOLADO_PATH)
print(df)