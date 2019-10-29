import matplotlib.pyplot as plt
import numpy as np

matrix_max = 153.832040129247
matrix_min = 43.2528741577922


def interpolate(v, color, dif):
    intervals = np.arange(0, 1.01, 1 / (len(color) - 1))
    for i in range(len(intervals) - 1):
        if intervals[i] <= v <= intervals[i + 1]:
            final = [0, 0, 0]
            for j in range(3):
                final[j] = (color[i + 1][j] - color[i][j]) * ((v - intervals[i]) * (1 / intervals[1])) + color[i][j]

            return dif*final[0]/255, dif*final[1]/255, final[2]/255


def gradient(v, dif):
    return interpolate(v, [(0, 255, 0), (255, 255, 0), (255, 0, 0)], dif)


def normalize(data, max_val, min_val):
    for i in range(len(data)):
        data[i] = (data[i] - min_val) / (max_val - min_val)
    return data


data = []
with open('big.dem', 'r') as f:
    f.readline()

    for line in f:
        data.append(normalize([float(l) for l in line.split()], matrix_max, matrix_min))


full = []
for i in range(len(data)):
    row = []
    for j in range(len(data[i])):
        dif = 1 - ((data[i - 1][j] - data[i][j]) * 6)
        row.append(gradient(data[i][j], dif))
    full.append(row)

plt.imshow(full)
plt.savefig("map.pdf")
plt.show()
