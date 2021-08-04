import pyvisa as visa
import time
import numpy as np


#Связь с осциллографом
visa_address = 'TCPIP::169.254.35.133::INSTR'
rm = visa.ResourceManager()
scope = rm.open_resource(visa_address)


scope.timeout = 10000
scope.chunk_size = 125000
print(scope.query('*IDN?'))
print(scope.query('*esr?'))
print(scope.query('allev?'))
rl = scope.query('horizontal:mode:recordlength?');
scope.write('DATA:ENCdg ASCii')
scope.write('wfmoutpre:byt_nr 2')
scope.write('data:stop ' + str(rl))
scope.write('data:source MATH1')
yoffset = float(scope.query('wfmoutpre:yoff?'))
ymult = float(scope.query('wfmoutpre:ymult?'))
yzero = float(scope.query('wfmoutpre:yzero?'))
scope.write('data:source MATH1')

# Основная программа
print('Введите класс')
cl = int(input())
print('Введите номер первой дальности')
dal_first = int(input())
print('Введите номер последней дальности')
dal_last = int(input())
data = np.zeros(1252) # подготавливаем массив для записи, 2 фичи: класс и номер дальности; 1250 отсчетов значений осциллограммы
for i in range(dal_first, dal_last + 1):
    print('Начинаем? Позиция ', i)
    print('Y/N')
    ans = str(input()).lower()
    if ans == 'y':
        for j in range(50): # берем 50 семплов
            time.sleep(0.01) # таймер между съемом осциллограмм
            raw_data = np.array(scope.query_ascii_values('CURV?')) # получаем осциллограмму 
            our_data = ((raw_data - yoffset) * ymult + yzero) # масштабируем 
            data = np.vstack((data, np.insert(our_data,0,[cl,i]))) # пишем в заготовленный массив данные, класс и дальность
    else:
        print('Перезапустите скрипт')
        break
data = data[1:]
path = r'C:\sig_data' # путь в папку сохранения
np.savetxt(path + "/" + str(cl) + '_' + str(dal_first) + '-' + str(dal_last) + ".csv", data, delimiter=",") # сохраняем на диске

print('СПАСИБО')
scope.close()
rm.close()