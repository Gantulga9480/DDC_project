import socket
import argparse
import select
from low_level_delay import delay_ms

parser = argparse.ArgumentParser()
parser.add_argument('msg', type=str)

args = parser.parse_args()

stm_addr = ('10.3.4.123', 11)
soc = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print('UDP Socket UP and sending')

# while 1:
# UDPClientSocket.sendto(str.encode('S1010101010'), serverAddressPort)
# delay(100)
# UDPClientSocket.sendto(str.encode('S0101010101'), serverAddressPort)
# delay(100)
soc.sendto('L'.encode(), stm_addr)
delay_ms(100)
soc.sendto(f'{args.msg}'.encode(), stm_addr)
delay_ms(100)
ready, _, _ = select.select([soc], [], [], 0.1)
if ready:
    data = soc.recv(4)
    print(data.hex())
soc.sendto('L'.encode(), stm_addr)
