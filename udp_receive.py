import socket
import select
import csv
import os
import argparse
from shutil import rmtree

parser = argparse.ArgumentParser()
parser.add_argument('ip', type=str, help='PC static IP')
parser.add_argument('port', type=int, help='PC receive PORT')
parser.add_argument('--show', action='store_const', const=True)
parser.add_argument('--silent', action='store_const', const=True)
parser.add_argument('--files', action='store')
parser.add_argument('--rows', action='store')
args = parser.parse_args()

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((args.ip, args.port))
print("UDP Socket up and listening")

P_MOD_PACKET_COUNT = args.rows if args.rows else 10000
TOTAL_FILES = args.files if args.files else 1
prev = 0
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


def udp_receive():
    ready, _, _ = select.select([UDPServerSocket], [], [], 0.05)
    if ready:
        msg = UDPServerSocket.recv(1008).hex()
        check_header(int(msg[1]))
        return msg
    return


if not args.show:
    try:
        try:
            rmtree('DDC_DATA')
        except FileNotFoundError:
            pass
        os.mkdir('DDC_DATA')
    except FileExistsError:
        print('Overwriting prev')

if not args.show:
    for i in range(TOTAL_FILES):
        try:
            with open(f'DDC_DATA/Data_{i+1}.csv', "w+", newline='') as _file:
                writer = csv.writer(_file)
                packet_count = 0
                print(f'FILES CREATED {i+1}')
                while packet_count < P_MOD_PACKET_COUNT:
                    packet_count += 1
                    try:
                        msg = udp_receive()
                        i_data = [hex2int(msg[i+2:i+4] + msg[i:i+2])
                                  for i in
                                  range(8, len(msg)-8, 8)]
                        q_data = [hex2int(msg[i+2:i+4] + msg[i:i+2])
                                  for i in
                                  range(12, len(msg)-8, 8)]
                        i_data.insert(0, int(msg[1]))
                        q_data.insert(0, int(msg[1]))
                        writer.writerow(i_data)
                        writer.writerow(q_data)
                        size += (len(str(i_data).replace(' ', '')))/1024/1024
                        size += (len(str(q_data).replace(' ', '')))/1024/1024
                    except Exception as e:
                        try:
                            rmtree('DDC_DATA')
                        except FileNotFoundError:
                            pass
                        print(e)
                        quit()
        except KeyboardInterrupt:
            break
    print(f'TOTAL FILES CREATED : {i+1}')
    print(f'TOTAL DATA CAPTURED : {round(size, 2)} MB')
else:
    while True:
        try:
            msg = udp_receive()
            if not args.silent:
                print(msg, '\n')
        except KeyboardInterrupt:
            break
