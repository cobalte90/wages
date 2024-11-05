import pandas as pd
import numpy as np

# Считываем wage.csv - таблицу с зарплатами
wage = pd.read_csv('wage.csv')

# Меняем значения пола с 0 и 1 на F и M
wage.gender = wage.gender.astype('object')
wage.loc[wage.gender == 0, 'gender'] = 'F'
wage.loc[wage.gender == 1, 'gender'] = 'M'

# Удаляем дубликаты
wage = wage.drop_duplicates()

# Удаляем строки, в которых значение зарплаты отрицательно
wage = wage[wage.wage >= 0]

# Проверяем корректность удаления
try:
    print(wage.loc[29]) # одна из строк с отрицательным значением зарплаты
except KeyError: print('True')

# Считываем таблицу с премиями
bonus = pd.read_csv('bonus.csv', sep=';')

# Джойним таблицы по person_id
df = pd.merge(wage, bonus, how="outer", on='person_id')

# Отсутствующие значения премми приравниванием к нулю
df.loc[df['bonus'].isnull(), 'bonus'] = 0

# В новой колонке total считаем 12 окладов и премию
df = df.assign(total = df.wage*12 + df.bonus)

# Выводим средние и медианные значения колонки total для женщин и мужчин
print(
    df.groupby('gender')['total'].agg(func=['mean', 'median'])
)

# Сохраняем датафрейм в файл 'df.csv'
df.to_csv('df.csv', index=False)

