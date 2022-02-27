import matplotlib.pylab as plt
import csv
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--fft', action='store_const', const=True)
args = parser.parse_args()


i_data = []
q_data = []

with open('DDC_DATA/Data_1.csv', 'r', newline='') as f:
    reader = csv.reader(f, delimiter=' ')
    for item in reader:
        d = item[0].split(',')
        a = [int(x) for x in d]
        i_data.append(a)


for item in i_data:
    if args.fft:
        power_i = np.abs(np.fft.rfft(np.array(item))) / len(item)
        # power_q = np.abs(np.fft.rfft(np.array(q))) / len(q)
        frequency = np.linspace(0, 300_000/2, len(power_i))
        plt.plot(frequency, power_i)
        # plt.plot(frequency, power_q)
    else:
        plt.plot(item)
        # plt.plot(q)
    plt.show()
