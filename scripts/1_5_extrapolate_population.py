import os

import pandas as pd

DATA_FOLDER = f'{os.getcwd()}/data'
HABS_PATH = f'{DATA_FOLDER}/habitantes.csv'
HABS_EXTRAPOLADO_PATH = f'{DATA_FOLDER}/habitantes_extrapolado.csv'
MONTHS = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGOS', 'SEP', 'OCT', 'NOV', 'DIC']
pd.set_option('display.max_columns', None)
try:
    habitantes_no_extrapolado = pd.read_csv(HABS_PATH)
    habitantes_diff = habitantes_no_extrapolado.diff()
except FileNotFoundError as e:
    print(f'Please run notebook/script 1_process_raw_data')
    raise e
year_index = habitantes_no_extrapolado.ANO.copy(deep=True)
df = pd.DataFrame(columns=MONTHS, index=habitantes_no_extrapolado.index)
# print(habitantes_diff)
for index, row in df.iterrows():
    for index_col, month in enumerate(MONTHS):
        if index == 0 and index_col < 7:
            df[month][index] = habitantes_no_extrapolado.reset_index(drop=True)['JUL'][index]
        elif index_col == 6:
            df[month][index] = habitantes_no_extrapolado.reset_index(drop=True)['JUL'][index]
        elif index_col > 6 and index < max(df.index):
            df[month][index] = df['JUL'][index] + (index_col - 6) * habitantes_diff.reset_index(drop=True)['JUL'][
                index + 1] / 12
        elif index_col > 6 and index == max(df.index):
            df[month][index] = df['JUL'][index]
        else:
            df[month][index] = df['JUL'][index - 1] + (index_col + 6) * habitantes_diff.reset_index(drop=True)['JUL'][
                index] / 12
df.set_index(year_index, inplace=True)
df.to_csv(HABS_EXTRAPOLADO_PATH)
