import pandas as pd
from io import StringIO
from csv import QUOTE_NONE
from pathlib import Path

fn = "t:\\Складской КОМПЛЕКС\\!МАРКИРОВКА\Арт-Логистик\\Уведомление заказ 28\\Маркировка\\Бартендер\\Коды\\"
fn += "Увр701_Заказ28_Акроброй Мозер 0,33_09.09.2026_6300.csv"

df = pd.DataFrame()
with open(fn, encoding='UTF-8') as file:
    csvString = file.readlines()
csvString = ''.join(csvString)
csvString = StringIO(csvString)
df = pd.read_csv(csvString, sep='\t', encoding='utf-8', dtype=object, header=None)
pallet = df[8].unique()
print(df[8].unique())