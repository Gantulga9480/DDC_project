import socket
from low_level_delay import delay

serverAddressPort = ("10.3.4.123", 8)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print('udp server ok')
bufferSize = 10
msgFromClient = ''
for i in range(bufferSize):
    msgFromClient += 'B'

# UDPClientSocket.sendto(bytesToSend, serverAddressPort)
index = 1
# while True:
ind = str(index)
msg = msgFromClient.replace('B', ind, 1)
bytesToSend = str.encode(msg)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
index += 1
if index == 9:
    index = 1
# delay(2.5)
