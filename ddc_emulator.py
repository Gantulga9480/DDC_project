import socket
from low_level_delay import delay
import numpy as np


serverAddressPort = ("127.0.0.1", 7)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

bufferSize = 1008

index = 1
while True:
    msgFromClient = str(index)
    for i in range(bufferSize-1):
        msgFromClient += str(np.random.randint(0, 9))
    ind = str(index)
    bytesToSend = str.encode(msgFromClient)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    index += 1
    if index == 9:
        index = 1
    delay(1)
