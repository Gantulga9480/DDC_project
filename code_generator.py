import csv

ch_count = 150
name = f'CH2_F_{ch_count}_'
defs = []
outs = []
c_count = 1

ff = open('raw.txt', 'w+')

with open('gg.csv', 'r', newline='') as f:
    reader = csv.reader(f, delimiter=' ')
    code = [item[0].split(',') for item in reader]
    # code = reader.__next__()[0].split(',')
    delay = code.pop()


def small(lst, d):
    global c_count
    out_code = []
    for i, item in enumerate(lst):
        if int(d[i]) > 500:
            count = int(d[i]) // 500
            for _ in range(count):
                out_code.append(str(item))
        else:
            out_code.append(str(item))

    defs.append(f'#define {name}{c_count}_D {len(out_code)}')
    # out = f'uint16_t {name}{c_count}[{name}{c_count}_D] = {{'
    out = f'uint16_t {name}{c_count}[{name}{c_count}_D] = {{'
    code = ', '.join(out_code)
    out += code
    out += '};'
    c_count += 1
    outs.append(out)


def big(code, delay):
    global c_count
    defs.append(f'#define {name}{c_count}_D {int(delay)//1_000_000}')
    out = f'uint16_t {name}{c_count} = {code};'
    c_count += 1
    outs.append(out)


last = []
last_delay = []

for c in code:
    # print('##################################################################')
    for i, item in enumerate(c):
        if int(delay[i]) > 1_000_000:
            if len(last) > 0:
                small(last, last_delay)
                last.clear()
                last_delay.clear()
            big(item, delay[i])
        else:
            last.append(item)
            last_delay.append(int(delay[i]))
    if len(last) > 0:
        small(last, last_delay)
        last.clear()
        last_delay.clear()

    for item in defs:
        print(item)

    for item in outs:
        ff.write(item+'\n')
        # print(item)
        # if input('resume? y/n:') == 'y':
        #     pass
        # else:
        #     break
    ch_count += 1
    c_count = 1
    defs.clear()
    outs.clear()
    name = f'CH1_F_{ch_count}_'

ff.close()
