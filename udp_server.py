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
        # address = bytesAddressPair[1]
        msg = message.hex()
        try:
            # header = int(msg[101:102])
            header = int(msg[1:2])
            # time = str(int(msg[120:122])-30) + str(int(msg[122:124])-30) + str(int(msg[124:126])-30) + str(int(msg[126:128])-30)
            # print(header)
        except Exception:
            pass

        if header == prev:
            print('loss')
            pass
        else:
            pass
        prev = header

        print(msg)
        # if header == 1:
        #     if 0 != prev:
        #         # pass
        #         print(f'loss at {prev} to {header} time {time}')
        #     prev = 0
        # else:
        #     if header - 1 != prev:
        #         # pass
        #         print(f'loss at {prev} to {header} time {time}')
        #     prev = header
    # quit()
