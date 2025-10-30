'''
Поиск совпадающих значений в двух файлах
  True   - количество совпадающих значений
  False  - количество уникальных значений 
'''

fn1 = 'c:\\Test BarTender\\1\\codesOrder_2025-10-17_08001250220028_2_SOL200R_1344.csv'
fn2 = 'c:\\Test BarTender\\1\\codesOrder_2025-10-17_08001250220028_2_SOL200R_2592.csv'

import pandas as pd
from io import StringIO
from pathlib import Path

pd.options.mode.copy_on_write = True

if str(Path(fn1).suffix) == '.csv':
    with open(fn1, encoding='UTF-8') as file:
        csvString = file.readlines()
    csvString = ''.join(csvString)
    csvString = StringIO(csvString)
    df1 = pd.read_csv(csvString, sep='\t', encoding='utf-8', dtype=object, header=None)
elif str(Path(fn1).suffix) == '.xlsx':
    df = pd.read_excel(fn1, dtype=object, header=None) 

if str(Path(fn2).suffix) == '.csv':
    with open(fn2, encoding='UTF-8') as file:
        csvString = file.readlines()
    csvString = ''.join(csvString)
    csvString = StringIO(csvString)
    df2 = pd.read_csv(csvString, sep='\t', encoding='utf-8', dtype=object, header=None)
elif str(Path(fn2).suffix) == '.xlsx':
    df = pd.read_excel(fn2, dtype=object, header=None) 

df1[1] = df2[0]
df1[2] = df1[1].isin(df1[0])

#df1[2] = df1[2] * 1
print(df1[2].value_counts())