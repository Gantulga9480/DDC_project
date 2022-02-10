import csv

SCALE = 50000
ORDER = 100

coef = []

with open('fir_coef.csv', newline='') as file:
    spamreader = csv.reader(file, delimiter=' ')
    for row in spamreader:
        coef.append(round(float(row[0]) * SCALE))

out = '    '
for item in coef:
    out += str(item) + ', '
print(f'int16_t DDC_FIR_COEF[RCF_SIZE] = {{')
print(out)
print('};')
