import pandas as pd
from io import StringIO
from pathlib import Path
import re


class Ranger():
    def __init__(self, file_path):
        try:
            self.file_path = file_path
            self.df = pd.DataFrame()
            with open(file_path, encoding='UTF-8') as file:
                csvString = file.readlines()
            csvString = ''.join(csvString)
            csvString = StringIO(csvString)
            self.df = pd.read_csv(csvString, sep='\t', encoding='utf-8', header=None, dtype=object)
            self.renamecolumns()
            #self.headers = ['N', 'GTIN', 'Code', 'CaseStart', 'CaseEnd', 'CaseSSCC', 'PalletStart', 'PalletEnd', 'PalletSSCC', 'MfgDate', 'ExpiryDate' ]
            #self.pallet_size = self.df['PalletSSCC'].value_counts()[0]
            #self.total_count = len(self.df)
            
            '''
            if 'PalletSSCC' in self.df.columns:
                self.df = self.df.drop_duplicates(subset=['MfgDate', 'PalletSSCC'], keep='first')
            elif 'CaseSSCC' in self.df.columns:
                self.df = self.df.drop_duplicates(subset=['MfgDate', 'CaseSSCC'], keep='first')
            '''
            if 'MfgDate' not in self.df.columns:
                self.df['MfgDate'] = '_'
            
            self.df['Order'] = Path(file_path).stem
            
            if '6' in self.df.columns:
                self.df['Range'] = (self.df['6'].astype(str)+'-'+self.df['7'].astype(str)).replace(' ','')
            
            elif '3' in self.df.columns:
                #self.df['6'] = self.df['3'].astype(int)
                #self.df['7'] = self.df['4'].astype(int)
                #self.df['7'] = (self.df['6']-1).astype(int)*self.pallet_size + self.pallet_size

                self.df['Range'] = (self.df['3'].astype(str)+'-'+self.df['4'].astype(str)).replace(' ','')
            self.df['Range'] = self.df['Range'].apply(self.trim_range)
            print(f'+ {Path(file_path).stem: <50} Total: {len(self.df)}')
        except:
            print(f'- {Path(file_path).stem: <50} Error')
        #pivottable.append(self.df)
        #print(self.df)        
        
        #table = pd.pivot_table(self.df, index=['MfgDate'], columns=['Range'], values= ['Code'], aggfunc=['count'])
        #+++++table = pd.pivot_table(self.df, index=['Order', 'MfgDate', 'Range'], values= ['Code'], aggfunc=['count'], sort=False)
        #+++++table = pd.pivot_table(self.df, index=['Order', 'MfgDate', 'PalletSSCC', 'Range'], values= ['Code'], aggfunc=['count'], sort=False)
        #table.stack().reset_index(inplace=True)
        #table.drop('count', axis=1, inplace=True)
        #print(table)

        #+++++table.to_excel(f'{Path(file_path).stem}.xlsx', header=None)
        #+++++pivottable.to_excel('print_range.xlsx', header=None)
        #print(pivottable)
        

    def renamecolumns(self):
        regGTIN = '^\\d{14}$'
        regCode = '^01\\d{14}21.*'
        regDateRU = '^(\\d{1,2})[-/.](\\d{1,2})[-/.](\\d{4})$'
        regDateEN = '^(\\d{4})[-/.](\\d{1,2})[-/.](\\d{1,2})$'
        regBox = '0{2}0\\d{17}'
        regPallet = '0{2}7\\d{17}'
        regStartRange = '^1$'


        #Удалаяем строку с заголовками если на есть
        while not pd.Series(self.df.iloc[0]).str.contains('^01\\d{14}21.*', regex=True).sum():
            self.df.drop(0, inplace=True)

        self.headers = []
        for col, item in enumerate(self.df.iloc[0].to_list()):
            if re.search(regGTIN, f'{item}'):
                self.headers.append('GTIN')
            elif re.search(regCode, f'{item}'):
                if '' in item:
                    self.headers.append('Code')
                else:
                    self.headers.append('CaseSSCC')
            elif re.search(regDateRU, f'{str(item)[:10]}') or re.search(regDateEN, f'{str(item)[:10]}'):
                if 'MfgDate' in self.headers:
                    self.headers.append('ExpiryDate')
                else:
                    self.headers.append('MfgDate')
            elif re.search(regBox, f'{item}'):
                self.headers.append('CaseSSCC')
            elif re.search(regPallet, f'{item}'):
                self.headers.append('PalletSSCC')
            else:
                self.headers.append(f'{col}')

        self.df.columns = self.headers
        self.df.reset_index(drop=True, inplace=True)

    def trim_range(self, s):
        return s.replace(' ','')

def main(current_dir):

    pd.options.mode.copy_on_write = True
    ranges = []
    for file_path in current_dir.glob('*.csv'):
        #print(f"Файл: {file_path}")
        print_range = Ranger(file_path)
        ranges.append(print_range.df)
    ranges = pd.concat(ranges, ignore_index=True)
    try:
        ranges = pd.pivot_table(ranges, index=['Order', 'MfgDate', 'PalletSSCC', 'Range'], values= ['Code'], aggfunc=['count'], sort=False)
        ranges.reset_index()
        ranges.to_excel(f'{Path(current_dir)}/print_range.xlsx', header=None)
    except:
        print('Нет данных по аггрегации')
    #print(ranges)

if __name__ == '__main__':
    work_dir = 'd:\\DM\\'
    current_order = 'VIT 658'
    main(Path(f'{work_dir}{current_order}'))