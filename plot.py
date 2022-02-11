import matplotlib.pylab as plt
import csv
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--fft', action='store_const', const=True)
args = parser.parse_args()


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
    i = item
    q = item = data.__next__()
    if args.fft:
        power_i = np.abs(np.fft.rfft(np.array(i))) / len(i)
        power_q = np.abs(np.fft.rfft(np.array(q))) / len(q)
        frequency = np.linspace(0, 300_000/2, len(power_i))
        plt.plot(frequency, power_i)
        plt.plot(frequency, power_q)
    else:
        plt.plot(i)
        plt.plot(q)
    plt.show()
