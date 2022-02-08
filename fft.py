import numpy as np
from matplotlib import pyplot as plt
import csv


def twosComplement_hex(hexval):
    bits = 16
    val = int(hexval, bits)
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val


sampling_rate = 39060


# time = np.linspace(0, np.pi*8, sampling_rate)
# datas = np.sin(2*np.pi*6*time)

datas = []

# with open('data.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ')
#     for row in spamreader:
#         for i in range(0, len(row), 2):
#             item = row[i+1] + row[i]
#             num = twosComplement_hex(item)
#             # print(num)
#             datas.append(num)

fourier_transform = np.fft.rfft(np.array(datas))

abs_fourier_transform = np.abs(fourier_transform)

power_spectrum = np.square(abs_fourier_transform)

frequency = np.linspace(0, sampling_rate/2, len(power_spectrum))

plt.plot(frequency, power_spectrum)
plt.show()
