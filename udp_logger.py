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
ddc1_header = None
ddc2_header = None
size = 0
data = ''


def check_header(msg):
    global ddc1_header, ddc2_header
    if msg[:8] == '41424142':
        if ddc1_header == '41424142':
            print('LOSS FOOTER')
        ddc1_header = '41424142'
    elif msg[:8] == '42414241':
        if ddc2_header == '42414241':
            print('LOSS FOOTER')
        ddc2_header = '42414241'
    elif msg[-8:] == '43444344':
        if ddc1_header == '43444344':
            print('LOSS HEADER')
        ddc1_header = '43444344'
    elif msg[-8:] == '44434443':
        if ddc2_header == '44434443':
            print('LOSS HEADER')
        ddc2_header = '44434443'


def hex2int(hexval):
    bits = 16
    val = int(hexval, 16)
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val


def udp_receive():
    ready, _, _ = select.select([UDPServerSocket], [], [], 0.01)
    if ready:
        msg = UDPServerSocket.recv(1024).hex()
        check_header(msg)
        return msg
    return


if not args.show:
    raise NotImplementedError
    try:
        try:
            rmtree('DDC_DATA')
        except FileNotFoundError:
            pass
        os.mkdir('DDC_DATA')
    except FileExistsError:
        print('Overwriting prev')
else:
    while True:
        try:
            msg = udp_receive()
            if not args.silent:
                print(msg, '\n')
        except KeyboardInterrupt:
            break
