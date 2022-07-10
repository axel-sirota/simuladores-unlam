import os

import pandas as pd

DATA_FOLDER = f'{os.getcwd()}/data'
VACUNADOS_PATH = f'{DATA_FOLDER}/preprocessed/vacunados.csv'
VACUNADOS_EXTRAPOLADO_PATH = f'{DATA_FOLDER}/extrapolated/vacunados_extrapolado.csv'
HABS_PATH = f'{DATA_FOLDER}/habitantes.csv'
MONTHS = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGOS', 'SEP', 'OCT', 'NOV', 'DIC']
pd.set_option('display.max_columns', None)
try:
    habitantes_no_extrapolado = pd.read_csv(HABS_PATH)
    vacunados_no_extrapolado = pd.read_csv(VACUNADOS_PATH)
except FileNotFoundError as e:
    print(f'Please run notebook/script 1_process_raw_data')
    raise e
initial_population = habitantes_no_extrapolado['JUL'][0]
year_index = habitantes_no_extrapolado.ANO.copy(deep=True)
df = pd.DataFrame(columns=MONTHS, index=habitantes_no_extrapolado.index)

for index, row in df.iterrows():
    for index_col, month in enumerate(MONTHS):
        if index == 0 and index_col == 0:
            df[month][index] = vacunados_no_extrapolado.reset_index(drop=True)[month][index] + initial_population
        elif index_col == 0:
            df['ENE'][index] = df['DIC'][index-1] + vacunados_no_extrapolado['ENE'][index]
        elif index_col > 0:
            df[month][index] = df[MONTHS[index_col-1]][index] + vacunados_no_extrapolado.reset_index(drop=True)[month][index]
df.set_index(year_index, inplace=True)
df.to_csv(VACUNADOS_EXTRAPOLADO_PATH)
