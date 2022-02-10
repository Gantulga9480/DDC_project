import matplotlib.pylab as plt
import csv


data = []

with open('DDC_DATA/Data_1.csv', 'r', newline='') as f:
    reader = csv.reader(f, delimiter=' ')
    for item in reader:
        d = item[0].split(',')
        d.pop(0)
        d = [int(x) for x in d]
        data.append(d)
        d = reader.__next__()[0].split(',')
        d.pop(0)
        d = [int(x) for x in d]
        data.append(d)

data = iter(data)
for item in data:
    plt.plot(item)
    print(len(item))
    item = data.__next__()
    print(len(item))
    plt.plot(item)
    plt.show()
