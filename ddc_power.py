import csv
import matplotlib.pyplot as plt

data = []
x = [-70, -65, -60, -55, -50, -45, -40, -35, -30, -25, -20, -15, -10, -5, 0]

with open('data.csv', 'r', newline='') as f:
    r = csv.reader(f, delimiter=' ')
    for item in r:
        data.append(int(item[0]))
    data.reverse()

plt.plot(x, data)
plt.show()
