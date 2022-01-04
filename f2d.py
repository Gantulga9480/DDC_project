import csv


coef = []

with open('coef128_3k_1.25Mhz.csv', newline='') as file:
    spamreader = csv.reader(file, delimiter=' ')
    for row in spamreader:
        coef.append(round(float(row[0]) * 1000))
        # print(round(float(row[0]) * 10))


out = ''

for item in coef:
    out += str(item) + ', '

print('int16_t coef[128] = {')
print(out)
print('};')
