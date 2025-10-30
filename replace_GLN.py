'''
Корректная замена GLN в файле базы данных/отчете
    fn      - файл для замены
    new_gln - новый GLN
'''
new_gln = "9998887770001"
fn = 't:\\Складской КОМПЛЕКС\\GrAnd\\test.txt'

#---------------------------------------------------------------------------------------------------
import pandas as pd
from io import StringIO
from csv import QUOTE_NONE
from pathlib import Path
from PyQt5.QtCore import QRegExp
from time import time

def replace_gln(s):
    new = s[0:3]+new_gln[:9]+s[12:19]
    s0 = 3*sum([int(x) for x in list(new)][::2])
    s1 = sum([int(x) for x in list(new)][1::2])
    return new+str((10 - (s0+s1) % 10) % 10)

start = time()
df = pd.DataFrame()
with open(fn, encoding='UTF-8') as file:
    csvString = file.readlines()
csvString = ''.join(csvString)
csvString = StringIO(csvString)
df = pd.read_csv(csvString, sep='\t', encoding='utf-8', dtype=object, header=None)
regSSCC = QRegExp('0{2}\\d{18}')

for i, item in enumerate(df.columns):
    if regSSCC.exactMatch(f'{item}'):
        df.iloc[:, i] = df.iloc[:, i].apply(replace_gln)
new_fn = f'{Path(fn).parent}/{Path(fn).stem}_newGLN.csv'
df.to_csv(new_fn, index=False, header=False, sep=chr(9), quoting=QUOTE_NONE)
print(f'+ Ok {new_fn}')
print(f'Время работы: {round(time()-start, 3)}c')
