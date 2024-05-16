import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

# Создание пользовательского цветового градиента между красным и зеленым цветами
colors = [(1, 0, 0), (0, 1, 0)]  # Красный и зеленый цвета
cmap_name = 'custom_gradient'
cm = LinearSegmentedColormap.from_list(cmap_name, colors)
threshold = 10
df = pd.read_csv("parse/13_blh.csv")
df_xyz = pd.read_csv("parse/13_xyz.csv")


def snr():
    dfsnr = pd.read_csv("parse/13_snr.csv")
    dfsnr = dfsnr.dropna(axis=1, how='all')  # Удаляем столбцы, где все значения NaN
    threshold = 0.3
    dfsnr = dfsnr.loc[:, (dfsnr != 0).mean() >= threshold]

    # Создаем график и добавляем все кривые на него
    plt.figure(figsize=(12, 8))
    for column in dfsnr.columns:
        if column != "Time":
            plt.scatter(dfsnr["Time"], dfsnr[column], label=column, s=1.5)

    plt.xlabel('Время, с', fontsize=14)
    plt.ylabel('Уровень сигнала', fontsize=14)
    plt.title('Уровень сигнала каждого спутника', fontsize=16)
    for spine in plt.gca().spines.values():
        spine.set_color('black')
        spine.set_linewidth(1.5)
    plt.grid(color='gray', alpha=0.7, linestyle='--')
    plt.gca().set_facecolor('white')

    plt.legend(markerscale=5)
    plt.savefig('png/Уровень.png', dpi=600)
    plt.grid(color='gray', alpha=0.5, linestyle='---')
    plt.savefig("png/color/Уровень.png", dpi=600)
    plt.show()


def rms():
    plt.figure(figsize=(12, 8))
    y_values = list(map(lambda y: float(y.replace(',', '.')), df["RMS, m"]))
    plt.scatter(df["Time"], y_values, s=15, color="green")

    plt.xlabel('Время, с', fontsize=14)
    plt.ylabel('СКО, м', fontsize=14)
    plt.title('СКО определения местоположения ГНСС', fontsize=16)
    for spine in plt.gca().spines.values():
        spine.set_color('black')
        spine.set_linewidth(1.5)
    plt.grid(color='gray', alpha=0.7, linestyle='--')
    plt.gca().set_facecolor('white')

    plt.savefig(f'png/СКО.png', dpi=600)
    plt.show()


def height():
    plt.figure(figsize=(12, 8))
    y_values = np.array(list(map(lambda y: float(y.replace(',', '.')), df["Height, m"])))
    time_values = np.array(list(df["Time"]))
    filtered_array = np.where((y_values >= -10) & (y_values <= 550))[0]
    y_values = y_values[filtered_array]
    y_values = y_values - y_values[0] + 9
    time_values = time_values[filtered_array]

    gaps = []
    for i in range(1, len(time_values)):
        if time_values[i] - time_values[i - 1] > 1:
            gaps.append(time_values[i - 1])
            gaps.append(time_values[i])

    for i in range(1, len(gaps), 2):
        plt.axvspan(gaps[i - 1], gaps[i], color='#ffff78')

    plt.scatter(time_values, y_values, s=5, color="green")

    plt.xlabel('Время, с', fontsize=14)
    plt.ylabel('Высота, м', fontsize=14)
    plt.title('Высота ЛА по данным ГНСС', fontsize=16)
    for spine in plt.gca().spines.values():
        spine.set_color('black')
        spine.set_linewidth(1.5)
    plt.grid(color='gray', alpha=0.7, linestyle='--')
    plt.gca().set_facecolor('white')

    last_time = time_values[-1]
    last_value = y_values[-1]
    plt.annotate(f'{round(last_value, 2)} м', xy=(last_time, last_value), xytext=(last_time, last_value + 0.2),
                 arrowprops=dict(facecolor='red', shrink=0.05), fontsize=12, color='red')
    plt.savefig(f'png/Высота.png', dpi=600)
    plt.show()


def trajectory():
    plt.figure(figsize=(12, 8))

    lat_values = [0] * len(df["Latitude"])
    lon_values = [0] * len(df["Longitude"])

    for i in range(len(df["Latitude"])):
        # Используем регулярное выражение для поиска чисел в строке
        matches = re.findall(r'\d+\.*\d*', df["Latitude"][i])
        degrees = float(matches[0])
        minutes = float(matches[1])
        seconds = float(matches[2] + "." + matches[3])
        # Рассчитываем итоговую координату
        lat_values[i] = degrees + minutes / 60 + seconds / 3600

        # Используем регулярное выражение для поиска чисел в строке
        matches = re.findall(r'\d+\.*\d*', df["Longitude"][i])
        degrees = float(matches[0])
        minutes = float(matches[1])
        seconds = float(matches[2] + "." + matches[3])
        # Рассчитываем итоговую координату
        lon_values[i] = degrees + minutes / 60 + seconds / 3600

    plt.scatter(lat_values, lon_values, s=1.5)

    plt.scatter(lat_values[0], lon_values[0], color='green', s=100, marker='o', edgecolors='black', linewidth=2)
    plt.scatter(lat_values[-1], lon_values[-1], color='red', s=100, marker='o', edgecolors='black', linewidth=2)

    plt.text(lat_values[0], lon_values[0] + 20, "ТВ", fontsize=16, color='green', ha='center')
    plt.text(lat_values[-1], lon_values[-1] + 20, "КТ", fontsize=16, color='red', ha='center')

    plt.xlabel('Широта, град', fontsize=14)
    plt.ylabel('Долгота, град', fontsize=14)
    plt.title('Траектория ЛА при посадке на аэродром по данным ГНСС', fontsize=16)
    for spine in plt.gca().spines.values():
        spine.set_color('black')
        spine.set_linewidth(1.5)
    plt.grid(color='gray', alpha=0.7, linestyle='--')
    plt.gca().set_facecolor('white')
    plt.savefig(f'png/Траектория.png', dpi=600)
    plt.show()


def kolvo_spt():
    plt.figure(figsize=(12, 8))
    list1 = list(df["Time"])
    gaps = []

    for i in range(1, len(list1)):
        if list1[i] - list1[i - 1] > 1:
            gaps.append(list1[i - 1])
            gaps.append(list1[i])

    for i in range(1, len(gaps), 2):
        plt.axvspan(gaps[i - 1], gaps[i], color='#ffff78')

    for i in range(len(df["Time"])):
        color_value = (df["NumSat"][i] - min(df["NumSat"])) / (
                max(df["NumSat"]) - min(df["NumSat"]))  # Вычисляем значение цвета для текущей точки
        plt.plot(df["Time"][i], df["NumSat"][i], marker='o', color=cm(color_value), markersize=3)

    plt.xlabel('Время, с', fontsize=14)
    plt.ylabel('Кол-во спутников', fontsize=14)
    plt.title('Количество спутников на всей траектории', fontsize=16)
    for spine in plt.gca().spines.values():
        spine.set_color('black')
        spine.set_linewidth(1.5)
    plt.grid(color='gray', alpha=0.7, linestyle='--')
    plt.gca().set_facecolor('white')

    last_time = df["Time"].iloc[-1]
    last_value = df["NumSat"].iloc[-1]
    plt.annotate(f'{df["Time"].iloc[len(df["Time"]) - 1]}', xy=(last_time, last_value),
                 xytext=(last_time, last_value), arrowprops=dict(facecolor='red', shrink=0.05))

    plt.savefig(f'png/Маяки.png', dpi=600)
    plt.show()


if __name__ == '__main__':
    # kolvo_spt()
    trajectory()
    height()
    # rms()
    # snr()
