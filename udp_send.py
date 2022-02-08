import socket
from low_level_delay import delay

serverAddressPort = ("10.3.4.28", 10)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print('UDP Socket UP and sending')

while 1:
    UDPClientSocket.sendto(str.encode('S1010101010'), serverAddressPort)
    delay(100)
    UDPClientSocket.sendto(str.encode('S0101010101'), serverAddressPort)
    delay(100)
    UDPClientSocket.sendto(str.encode('L'), serverAddressPort)
    delay(100)
