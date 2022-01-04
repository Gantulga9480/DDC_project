import socket
from tkinter import *
from tkinter import ttk


class DDC(Tk):

    IP = "10.3.4.28"
    PORT = 7
    SERVER_IP = "10.3.4.123"
    SERVER_PORT = 8

    def __init__(self, screenName=None, baseName=None,
                 useTk=1, sync=0, use=None):
        super().__init__(screenName=screenName, baseName=baseName,
                         useTk=useTk, sync=sync, use=use)

        self.UDP_read_soc = socket.socket(family=socket.AF_INET,
                                          type=socket.SOCK_DGRAM)
        self.UDP_write_soc = socket.socket(family=socket.AF_INET,
                                           type=socket.SOCK_DGRAM)

        self.e1 = ttk.Entry(self)
        self.e1.grid(row=0, column=0)
        self.e2 = ttk.Entry(self)
        self.e2.grid(row=0, column=1)

        self.btn = ttk.Button(self, text="Test")
        self.btn.grid(row=1, column=0, columnspan=2)

        self.udp_receive()
        self.mainloop()

    def udp_send(self):
        pass

    def udp_receive(self):
        bytesAddressPair = UDP_read_soc.recvfrom(bufferSize)
        self.after(100, self.udp_receive)

    def connect_ddc(self):
        pass


DDC()
