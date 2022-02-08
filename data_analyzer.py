import csv


path = r'LDATA\data logger 10_20\12t32t34\LA1232_0.csv'
data = []
data1 = []

with open(path, newline='') as file:
    reader = csv.reader(file, delimiter=' ')
    reader.__next__()
    reader.__next__()
    for row in reader:
        # print(row[0].split(',')[0])
        data.append(row[0].split(',')[0])
        data1.append(row[0].split(',')[1])


for i in range(len(data)-2):
    time = 0
    n_time = 0
    if data[i][-2] == 'm':
        time = float(data[i][0:-2])
        # print(time)
    else:
        time = float(data[i][0:-1])*1000
    if data[i+1][-2] == 'm':
        n_time = float(data[i+1][0:-2])
        # print(n_time)
    else:
        n_time = float(data[i+1][0:-1])*1000

    diff = (n_time - time) * 1_000_000
    if diff > 100_000_000:
        print('delay')
    elif diff > 1000:
        print('odd 1000')
        print(f'{bin(int(data1[i-1]))} -> {bin(int(data1[i]))} -> {bin(int(data1[i+1]))}')
    elif diff < 100:
        print('odd 100')
        print(f'{bin(int(data1[i-1]))} -> {bin(int(data1[i]))} -> {bin(int(data1[i+1]))}')
    else:
        print(diff, 'ns')
