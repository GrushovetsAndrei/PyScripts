'''
Разделитель исходных кодов на произвольное количество наборов необходимой длины
  parts - список размеров наборов
  fn    - файл с исходными кодами
  !  Контроль по размерности списка и исходного набора, а также на уникальность 
  кодов в исходном наборе кодов
'''
#Количество кодов в каждой дате
parts = [2016]
fn = 't://Складской КОМПЛЕКС//!МАРКИРОВКА//Арт-Логистик//Уведомление 686 заказ Косметика 11852_021414//маркировка//18040 MILMIL Шампунь детский  Абрикос 500мл (ЧЗ) Заказ КМ 00МА-000063.txt'

#-----------------------------------------------------------------------------------------------------
import pandas as pd
from io import StringIO
from csv import QUOTE_NONE
from pathlib import Path
from time import time

start = time()
df = pd.DataFrame()

if str(Path(fn).suffix) == '.csv' or str(Path(fn).suffix) == '.txt':
    with open(fn, encoding='UTF-8') as file:
        csvString = file.readlines()
    csvString = ''.join(csvString)
    csvString = StringIO(csvString)
    df = pd.read_csv(csvString, sep='\t', encoding='utf-8', dtype=object, header=None)
elif str(Path(fn).suffix) == '.xlsx':
    df = pd.read_excel(fn, dtype=object, header=None) 

if len(df) == sum(parts):
    for part in parts:
        try:
            df_part = df[:part]
            new_fn = f'{Path(fn).parent}/{Path(fn).stem}_{part}.csv'
            df_part.to_csv(new_fn, index=False, header=False, sep=chr(9), quoting=QUOTE_NONE)
            df = df[part:]
            print(f'+ Ok {new_fn}')
        except:
            print('- Error')
else:
    print('ВНИМАНИЕ! Неверная сумма частей.')
if len(df) != len(df[0].unique()):
    print('!!!!! В исходном наборе есть повторяющиеся коды.')
print(f'Время работы: {round(time()-start, 3)}c')