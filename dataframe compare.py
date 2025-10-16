'''
Поиск совпадающих значений в двух файлах
  True   - количество совпадающих значений
  False  - количество уникальных значений 
'''

fn1 = 'd:\\WA\\327 Сливки\\Master Gourmet.csv'
fn2 = 'd:\\WA\\327 Сливки\\AG5ATD Martini Plus Sfoglia 1413 кодов.csv'
































import pandas as pd
import numpy as np
from io import StringIO



pd.options.mode.copy_on_write = True

with open(fn1, encoding='UTF-8') as file:
    csvString = file.readlines()
csvString = ''.join(csvString)
csvString = StringIO(csvString)
df1 = pd.read_csv(csvString, sep='\t', encoding='utf-8', dtype=object, header=None)

with open(fn2, encoding='UTF-8') as file:
    csvString = file.readlines()
csvString = ''.join(csvString)
csvString = StringIO(csvString)
df2 = pd.read_csv(csvString, sep='\t', encoding='utf-8', dtype=object, header=None)
df1[1] = df2[0]
df1[2] = df1[1].isin(df1[0])
#df1[2] = df1[2] * 1
print(df1[2].value_counts())