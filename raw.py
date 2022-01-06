import csv
from matplotlib import pyplot as plt


def twosComplement_hex(hexval):
    bits = 16
    val = int(hexval, 16)
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val


datas = []

with open('data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        for i in range(0, len(row), 2):
            item = row[i+1] + row[i]
            num = twosComplement_hex(item)
            # print(num)
            datas.append(num)

plt.plot(datas)
plt.show()
