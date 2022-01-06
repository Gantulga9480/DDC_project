import socket
from collections import deque
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread


def twosComplement_hex(hexval):
    bits = 16
    val = int(hexval, 16)
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val


def udp(i):
    ax.cla()
    bytesAddressPair = UDPServerSocket.recv(bufferSize)
    message = bytesAddressPair
    msg = message.hex()
    data = [twosComplement_hex(msg[i+2:i+4] + msg[i:i+2]) for i in range(16, len(msg)-16, 4)]

    # print(data)

    plt.plot(data)


localIP = "10.3.4.28"
localPort = 7
bufferSize = 1024

buf = deque(maxlen=20)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

prev = 0
p_idx = 0

fig = plt.figure()
ax = plt.subplot()
# animate
ani = FuncAnimation(fig, udp, interval=0)
plt.show()
