from datetime import datetime

import chardet
import pandas as pd


path1 = "files/северка_13_02/13_snr.csv"
path2 = "files/северка_13_02/13_snr_2.csv"
path3 = "parse/13_snr.csv"

def txt_to_df(path):
    # Определяем кодировку файла
    with open(path, 'rb') as file:
        rawdata = file.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']

    with open(path, 'r', encoding=encoding) as file:
        lines = file.readlines()
        while lines[-1] == '' or lines[-1] == '\n':
            lines.pop()

    index = None
    for i, line in enumerate(lines):
        if 'No' in line:
            index = i
            break

    my_list = list(map(str.strip, lines[index].strip().split("|")))
    len_lists = len(lines[index+2:])

    my_dict = {key: [None] * len_lists for key in my_list}

    for i in range(len_lists):
        temp_list = list(map(str.strip, lines[i+index+2].strip().split("|")))
        for j, key in enumerate(my_dict.keys()):
            my_dict[key][i] = temp_list[j]


    return pd.DataFrame(my_dict)

# df1 = txt_to_df(path1)
# df1.drop("No", axis=1, inplace=True)
# df2 = txt_to_df(path2)
# df2.drop("No", axis=1, inplace=True)

df1 = pd.read_csv(path1, sep=";")
df2 = pd.read_csv(path2, sep=";")

df = pd.concat([df1, df2], ignore_index=True)
df["Time"] = df["Time"].apply(lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S.%f"))
# Находим разницу во времени между каждым значением и первым значением
df["Time"] = (df["Time"] - df["Time"].iloc[0]).dt.total_seconds()
# Округляем значение времени до одного знака после запятой
df["Time"] = df["Time"].round(1)
# Сохраняем столбец "Time Delta" в отдельную переменную
time_delta = df["Time"]
# Удаляем столбец "Time Delta" из DataFrame
df = df.drop(columns=["Time"])
# Вставляем столбец "Time Delta" в начало DataFrame
df.insert(0, "Time", time_delta)
# df.drop("UTC time", axis=1, inplace=True)
df.to_csv(path3, index=False)