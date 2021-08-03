import pandas as pd
import glob
import os

path = r'C:\sig_data' # путь в папку чтения и сохранения
all_files = glob.glob(path + "/*.csv") # получаем список файлов для объединения

li = [] # временный массив для объединения

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=None)
    li.append(df) # добавляем датасеты в один общий

frame = pd.concat(li, axis=0, ignore_index=True)

for f in all_files:
    os.remove(f)
frame.to_csv(path+'/data.csv',index=False) # пишем в файл