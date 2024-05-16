import matplotlib.pyplot as plt
import numpy as np

# Генерация данных на временной прямой
time = np.arange(0, 10, 0.1)  # временная прямая с шагом 0.1
data = np.sin(time)  # пример данных, можно заменить на свои

# Создание графика
plt.figure(figsize=(12, 6))
plt.plot(time, data, color='blue')  # построение графика данных

# Выделение зон без данных желтым цветом
gaps = [2.5, 4.5]  # пример зон без данных, можно заменить на свои
for i in range(0, len(gaps), 2):
    plt.axvspan(gaps[i], gaps[i+1], color='yellow', alpha=0.3)

plt.xlabel('Время')
plt.ylabel('Данные')
plt.title('График данных на временной прямой с выделенными зонами без данных')
plt.grid(True)
plt.show()
list1 = []
list2 = []
for i in range(1, len(list1)):
    if list1[i] - list1[i-1] > 0.1:
        list2.append(list1[i-1])
        list2.append(list1[i])
