import csv
import matplotlib.pylab as plt
import numpy as np


def twosComplement(intval):
    bits = 16
    val = intval << 6
    if val & (1 << (bits - 1)):
        val -= 1 << bits
    return val


data = []
time = []
val = 0

with open('adc.csv', newline='') as file:
    csv_file = csv.reader(file, delimiter=' ')
    for row in csv_file:
        # print(row)
        try:
            item = row[0].split(',')
            t = float(item[0].split('ns')[0])
            t /= 1000
            time.append(t)
            val = twosComplement(int(item[1]))
            data.append(val)
        except Exception:
            try:
                item = row[0].split(',')
                t = float(item[0].split('us')[0])
                time.append(t)
                val = twosComplement(int(item[1]))
                data.append(val)
            except Exception:
                try:
                    item = row[0].split(',')
                    t = float(item[0].split('ms')[0])
                    t *= 1000
                    time.append(t)
                    val = twosComplement(int(item[1]))
                    data.append(val)
                except Exception:
                    pass
        if val < -10000:
            print(val)
            print(row)

plt.plot(time, data)
plt.show()
