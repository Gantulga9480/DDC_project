import socket
import select
import csv

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind(("10.3.4.28", 10))

print("UDP SOCKET up and listening")

prev = 0
P_MOD_PACKET_COUNT = 100

writer = csv.writer()

while(True):
    ready, _, _ = select.select([UDPServerSocket], [], [], 0.05)
    if ready:
        msg = UDPServerSocket.recv(1008).hex()
        try:
            header = int(msg[1:2])
            # print(header)
        except Exception:
            quit()

        if header == 1:
            prev = 1
        else:
            if header - 1 != prev:
                print(f'loss at {prev} to {header}')
            prev = header
