import glob
import pandas as pd
from io import StringIO
from csv import QUOTE_NONE, writer as csv_writer
from pathlib import Path
from progress.bar import IncrementalBar

# Укажите путь к папке и маску файла (например, все .csv файлы)
folder_path = "t:/Складской КОМПЛЕКС/!МАРКИРОВКА/Арт-Логистик/Уведомление 729 заказ Косметика 021951/Маркировка/Коды маркировки/Бартендер/"
mask = "*.csv"

full_path = f"{folder_path}/{mask}"
bar = IncrementalBar('Progress', max = len(glob.glob(full_path)))
# Перебираем файлы, соответствующие маске
for file_path in glob.glob(full_path):
    bar.next()
    df = pd.DataFrame()
    with open(file_path, encoding='UTF-8') as file:
        csvString = file.readlines()
    csvString = ''.join(csvString)
    csvString = StringIO(csvString)
    df = pd.read_csv(csvString, sep='\t', encoding='utf-8', dtype=object, header=None)
    pallet = pd.DataFrame(df[5].unique(), columns=['CaseSSCC'])
    output_file = Path(f'{Path(file_path).parent}/Короба/{Path(file_path).name}')
    output_file.parent.mkdir(exist_ok=True, parents=True)                
    pallet.to_csv(output_file, index=False, sep=chr(9), quoting=QUOTE_NONE, header=None)
    
bar.finish()