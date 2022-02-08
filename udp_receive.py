import socket
import select
import csv
import os

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind(("10.3.4.28", 10))

print("UDP SOCKET up and listening")

prev = 0
P_MOD_PACKET_COUNT = 10000

file_id = 1

size = 0


def check_header(header):
    global prev
    if header == 1:
        prev = 1
    else:
        if header - 1 != prev:
            print(f'LOSS at {prev} to {header}')
        prev = header

def hex2int(hexval):
    bits = 16
    val = int(hexval, 16)
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val


try:
    os.mkdir('DDC_DATA')
except FileExistsError:
    print('Overwriting prev')

while True:
    try:
        with open(f'DDC_DATA/Data_{file_id}.csv', "w+", newline='') as _file:
            writer = csv.writer(_file)
            packet_count = 0
            while packet_count < P_MOD_PACKET_COUNT:
                ready, _, _ = select.select([UDPServerSocket], [], [], 0.05)
                if ready:
                    packet_count += 1
                    msg = UDPServerSocket.recv(1008).hex()
                    try:
                        header = int(msg[1])
                        # print(len(msg))
                        check_header(header)
                        i_data = [hex2int(msg[i+2:i+4] + msg[i:i+2])
                                  for i in
                                  range(8, len(msg)-8, 8)]
                        q_data = [hex2int(msg[i+2:i+4] + msg[i:i+2])
                                  for i in
                                  range(12, len(msg)-8, 8)]
                        i_data.insert(0, header)
                        q_data.insert(0, header)
                        writer.writerow(i_data)
                        writer.writerow(q_data)
                        size += len(i_data) / 1024 / 1024 * 2
                        # print(header)
                    except Exception:
                        print('Header error!')
                        quit()
        file_id += 1
        print()
    except KeyboardInterrupt:
        break

print(f'TOTAL FILES CREATED : {file_id}')
print(f'TOTAL DATA CAPTURED : {size} MB')
