# 1-D-CNN-Multilabel-Classification

## Ссылка
Main: [1-D-CNN-Multilabel-Classification](https://github.com/svvema/1-D-CNN-Multilabel-Classification/blob/main/signal_work.ipynb)

## Используемые библиотеки
*pandas, torch, matplotlib, numpy, csv, sklearn.model_selection, zipfile, pyvisa*

# Задача

Имеется макет устройства, осуществляющий одновременное излучение и прием радиосигнала. 
В результате работы макета получаем осциллограмму радиосигнала, отображающую изменение амплитуды сигнала во времени.
Полученная осциллограмма является суммой сигнала прямого излучения и эхо-сигнала, отраженного от цели. 
Цели могут быть разные, соответственно конфигурация эхо-сигнала тоже будет разной, также цели могут находиться на разном расстоянии от излучателя.

Таким образом задача состоит в том, чтобы научиться распознавать полученные осциллограммы, т.е. понять какой объект находится перед макетом и на каком расстоянии.

# Ход решения

Данная задача по своей сути является задачей классификации одномерного ряда, таким образом её можно решить путем использования сверточных нейронных сетей.
Было принято решение использовать мультилейбл из предположения, если система не сможет распознать объект с достаточной долей достоверности, то мы хотя бы получим информацию на каком он расстоянии.
Поскольку в датасете применяется OHE кодирование для задания класса и дальности двумя фичами, получаем всего 17 разных классов (см. таблицу в разделе данные), поэтому на выходе полносвязного слоя сверточной сети будем предсказывать 17 вероятностей.
За основу архитектуры сети была выбрана модель LeNet с определенными улучшениями:
| № | Слой | Kernel | in | out | padding | stride |
| :-- | :------ | :------ | :------ | :------ | :------ | :------ |
| 1 | Conv1d | 5 | 1 | 12 | 0 | 1 |
| 2 | ReLU | - | - | - | - | - |
| 3 | MaxPool1d | 2 | 12 | 12 | 0 | 2 |
| 4 | Conv1d | 3 | 12 | 36 | 0 | 1 |
| 5 | ReLU | - | - | - | - | - |
| 6 | MaxPool1d | 2 | 36 | 36 | 0 | 2 |

Далее идут полносвязные слои:
| № | Слой | in | out |
| :-- | :------ | :------ | :------ |
| 1 | Linear | 11160 | 2697 |
| 2 | ReLU | - | - |
| 3 | Linear | 2697 | 84 |
| 4 | ReLU | - | - |
| 5 | Linear | 84 | 17 |

Поскольку данная задача относится к мультилейбл классификации, в качестве функции потерь используем BCEWithLogitsLoss.
Используемый оптимайзер -- Adam.
Метрика для отслеживания качества обучения -- accuracy.

## Данные

В результате работы макета имеем одномерный вектор значений амплитуд сигнала по 1500 отсчетам.
Заранее зададимся таблицей классов. Имеем 5 классов объектов, находящихся на 10 разных дальностях и 1 класс с нулевой дальностью, т.е. когда объекта нет перед макетом.
| № | Объект | Класс | Диапазон дальностей|
| :-- | :---------------------- | :---------------------- | :---------------------- |
| 1 | Нет Объекта | 0 | 0 |
| 2 | Объект №1 | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| 3 | Объект №2 | 2 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| 4 | Объект №3 | 3 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| 5 | Объект №4 | 4 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| 6 | Объект №5 | 5 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |

Для формирования датасета были написаны небольшие программы скрипты на .py выполняющие следующие действия:
- snimok.py: 
Программа формирования датасета осциллограмм объекта. Программа позволяет задать класс объекта и диапазон дальностей для сбора 50 образцов сигнала объекта на каждую дальность, далее происходит запись полученного датасета в формате CSV на жесткий диск.
- add_db.py: 
Программа объединяющая полученные датасеты по объектам в единый датасет, с дальнейшей его архивацией.

Структура датасета следующая:
- 0 столбец: класс объекта;
- 1 столбец:  дальность объекта;
- Столбцы с 2 по 1501:  значение амплитуд сигнала по отсчетам.


