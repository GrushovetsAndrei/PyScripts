'''
Поиск совпадающих значений в двух файлах
  True   - количество совпадающих значений
  False  - количество уникальных значений 
'''

fn1 = 't:\\Складской КОМПЛЕКС\\GrAnd\\test.txt'
fn2 = 't:\\Складской КОМПЛЕКС\\GrAnd\\test2.txt'

import pandas as pd
from io import StringIO


pd.options.mode.copy_on_write = True

with open(fn1, encoding='UTF-8') as file:
    csvString = file.readlines()
csvString = ''.join(csvString)
csvString = StringIO(csvString)
#С заголовками
#df1 = pd.read_csv(csvString, sep='\t', encoding='utf-8', dtype=object)
#Без заголовков
df1 = pd.read_csv(csvString, sep='\t', encoding='utf-8', dtype=object, header=None)
with open(fn2, encoding='UTF-8') as file:
    csvString = file.readlines()
csvString = ''.join(csvString)
csvString = StringIO(csvString)
df2 = pd.read_csv(csvString, sep='\t', encoding='utf-8', dtype=object, header=None)

#Добавить последним столбцом данные для сравнения (2 - номер столбца в df2 для сравнения)
df1[len(df1.columns.to_list())] = df2[2]
#Сравнение данных в столбцах и сохрание резхзультата сравнения в столбце Compare
df1['Compare'] = df1[2].isin(df1[len(df1.columns.to_list())-1])

print(df1['Compare'].value_counts())
print(f'Совпадающие коды: {df1['Compare'].value_counts()[True]}')
print(list(df1[df1['Compare']==True][2]))
