import socket
import select
import csv
import os
import argparse
import sys
from shutil import rmtree

parser = argparse.ArgumentParser()
parser.add_argument('ip', type=str, help='PC static IP')
parser.add_argument('port', type=int, help='PC receive PORT')
parser.add_argument('--iq', action='store_const', const=True)
parser.add_argument('--show', action='store_const', const=True)
parser.add_argument('--silent', action='store_const', const=True)
parser.add_argument('--files', action='store', type=int)
parser.add_argument('--rows', action='store', type=int)
args = parser.parse_args()

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((args.ip, args.port))
print("UDP Socket up and listening")

P_MOD_PACKET_COUNT = args.rows if args.rows else 10000
TOTAL_FILES = args.files if args.files else 1
prev = 0
size = 0
data = ''


def check_header(msg):
    global prev
    if msg[:8] == '41424142':
        if prev == '41424142':
            print('LOSS FOOTER')
        prev = '41424142'
    else:
        if msg[-8:] == '43444344':
            if prev == '43444344':
                print('LOSS HEADER')
        prev = '43444344'


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
        check_header(msg)
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
                print(f'FILE {i+1}')
                while packet_count < P_MOD_PACKET_COUNT:
                    try:
                        msg = udp_receive()
                        if args.iq:
                            raise NotImplementedError
                        else:
                            if prev == '43444344':
                                data += [hex2int(msg[i+2:i+4] + msg[i:i+2])
                                         for i in
                                         range(0, len(msg)-8, 4)]
                                writer.writerow(data)
                                size += (len(str(data).replace(' ', ''))) \
                                    / 1024 / 1024
                                packet_count += 1
                            elif prev == '41424142':
                                data = [hex2int(msg[i+2:i+4] + msg[i:i+2])
                                        for i in
                                        range(12, len(msg), 4)]
                    except Exception as e:
                        try:
                            rmtree('DDC_DATA')
                        except FileNotFoundError:
                            pass
                        print(e)
                        sys.exit()
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
