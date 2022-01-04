import socket
from collections import deque

localIP = "10.3.4.28"
localPort = 7
bufferSize = 1024

buf = deque(maxlen=20)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

HEADER_SIZE = 4

prev = 0

while(True):
    bytesAddressPair = UDPServerSocket.recv(bufferSize)
    UDPServerSocket.sendto
    message = bytesAddressPair
    # address = bytesAddressPair[1]
    msg = message.hex()
    try:
        header = int(msg[1:2])
    except Exception:
        quit()

    if header == 8:
        if header - 1 != prev:
            print(f'loss at {prev} to {header}')
        prev = 0
    else:
        if header - 1 != prev:
            print(f'loss at {prev} to {header}')
        prev = header
