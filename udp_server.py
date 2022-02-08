import socket
import select

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind(("10.3.4.28", 10))

print("UDP server up and listening")

HEADER_SIZE = 4

prev = 0

while(True):
    ready, _, _ = select.select([UDPServerSocket], [], [], 0.05)
    if ready:
        bytesAddressPair = UDPServerSocket.recv(1100)
        message = bytesAddressPair
        msg = message.hex()
        try:
            header = int(msg[1:2])
            print()
            print(msg[8:2008])
            # print(header)
        except Exception:
            quit()

        # if header == prev:
        #     print(f'loss {prev} to {header}')
        # else:
        #     pass
        # prev = header
        # print(msg)
        if header == 1:
            prev = 1
        else:
            if header - 1 != prev:
                print(f'loss at {prev} to {header}')
            prev = header
    # quit()
