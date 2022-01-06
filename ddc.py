import socket
import numpy as np
from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from DDC_REGS import *


class DDC(Tk):

    PC_IP = "10.3.4.28"
    PC_PORT = 7
    DDC_IP = "10.3.4.123"
    DDC_PORT = 8
    BUFFER_SIZE = 1024

    def __init__(self, screenName=None, baseName=None,
                 useTk=1, sync=0, use=None) -> None:
        super().__init__(screenName=screenName, baseName=baseName,
                         useTk=useTk, sync=sync, use=use)

        self.d300_var = StringVar()

        self.UDP_server_soc = socket.socket(family=socket.AF_INET,
                                            type=socket.SOCK_DGRAM)

        self.resizable(False, False)

        self.d300l = ttk.Label(self, text='DDC MODE            ')
        self.d301l = ttk.Label(self, text='NCO MODE            ')
        self.d302l = ttk.Label(self, text='NCO SYNC MASK       ')
        self.d303l = ttk.Label(self, text='NCO FREQUENCY       ')
        self.d304l = ttk.Label(self, text='NCO PHASE OFFSET    ')
        self.d305l = ttk.Label(self, text='CIC2 SCALE          ')
        self.d306l = ttk.Label(self, text='CIC2 DECIMATION (-1)')
        self.d307l = ttk.Label(self, text='CIC5 SCALE          ')
        self.d308l = ttk.Label(self, text='CIC5 DECIMATION (-1)')
        self.d309l = ttk.Label(self, text='RCF SCALE           ')
        self.d30Al = ttk.Label(self, text='RCF DECIMATION  (-1)')
        self.d30Bl = ttk.Label(self, text='RCF ADDRESS OFFSET  ')
        self.d30Cl = ttk.Label(self, text='RCF FILTER TAPS (-1)')
        self.d300e = ttk.Entry(self)

        self.d300_menu = ttk.Combobox(self,
                                      value=D300_OPT,
                                      textvariable=self.d300_var)
        self.d300_menu.current(0)
        self.d300_menu.config(state="readonly", width=22)
        self.d300_menu.bind("<<ComboboxSelected>>")

        self.d301e = ttk.Entry(self)
        self.d302e = ttk.Entry(self)
        self.d303e = ttk.Entry(self)
        self.d304e = ttk.Entry(self)
        self.d305e = ttk.Entry(self)
        self.d306e = ttk.Entry(self)
        self.d307e = ttk.Entry(self)
        self.d308e = ttk.Entry(self)
        self.d309e = ttk.Entry(self)
        self.d30Ae = ttk.Entry(self)
        self.d30Be = ttk.Entry(self)
        self.d30Ce = ttk.Entry(self)

        self.btn_frame = ttk.Frame(self)

        self.con_btn = ttk.Button(self.btn_frame, text="Connect",
                                  command=self.connect_ddc)
        self.send_btn = ttk.Button(self.btn_frame, text="Send",
                                   command=self.send_btn_command)
        self.graph_btn = ttk.Button(self.btn_frame, text="FFT",
                                    command=self.graph_btn_command)

        self.fig = plt.figure()
        self.graph = plt.subplot()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()

        self.graph_nav_l = ttk.Label(self, text='Set interval (max = 500)')
        self.graph_nav_e = ttk.Entry(self)
        self.graph_nav_btn = ttk.Button(self, text="Set",
                                        command=self.graph_nav_btn_command)

        self.d300l.grid(row=0, column=0, sticky=W)
        # self.d300e.grid(row=0, column=1)
        self.d300_menu.grid(row=0, column=1, columnspan=2, pady=5)
        self.d301l.grid(row=1, column=0, sticky=W)
        self.d301e.grid(row=1, column=1)
        self.d302l.grid(row=2, column=0, sticky=W)
        self.d302e.grid(row=2, column=1)
        self.d303l.grid(row=3, column=0, sticky=W)
        self.d303e.grid(row=3, column=1)
        self.d304l.grid(row=4, column=0, sticky=W)
        self.d304e.grid(row=4, column=1)
        self.d305l.grid(row=5, column=0, sticky=W)
        self.d305e.grid(row=5, column=1)
        self.d306l.grid(row=6, column=0, sticky=W)
        self.d306e.grid(row=6, column=1)
        self.d307l.grid(row=7, column=0, sticky=W)
        self.d307e.grid(row=7, column=1)
        self.d308l.grid(row=8, column=0, sticky=W)
        self.d308e.grid(row=8, column=1)
        self.d309l.grid(row=9, column=0, sticky=W)
        self.d309e.grid(row=9, column=1)
        self.d30Al.grid(row=10, column=0, sticky=W)
        self.d30Ae.grid(row=10, column=1)
        self.d30Bl.grid(row=11, column=0, sticky=W)
        self.d30Be.grid(row=11, column=1)
        self.d30Cl.grid(row=12, column=0, sticky=W)
        self.d30Ce.grid(row=12, column=1)
        self.btn_frame.grid(row=13, column=0, columnspan=2)
        self.canvas.get_tk_widget().grid(column=4, row=0, rowspan=13, columnspan=3)
        self.graph_nav_l.grid(row=13, column=4, sticky=NS)
        self.graph_nav_e.grid(row=13, column=5, sticky=NSEW)
        self.graph_nav_btn.grid(row=13, column=6, sticky=NS)
        self.con_btn.grid(row=0, column=0, padx=3)
        self.send_btn.grid(row=0, column=1, padx=3)
        self.graph_btn.grid(row=0, column=2, padx=3)

        self.fclock = 5 * 10**6
        self.total_decimation = 128
        self.fsamp = int(self.fclock / self.total_decimation)

        self.is_con = False
        self.is_fft = False
        self.is_graph = True

        self.graph_erase_len = 0

        self.draw_ddc()
        self.mainloop()

    def draw_ddc(self):
        self.graph.cla()
        data = []
        if self.is_con and self.is_graph:
            byteData = self.UDP_server_soc.recv(self.BUFFER_SIZE)
            msg = byteData.hex()
            data = [self.hex2int(msg[i+2:i+4] + msg[i:i+2]) for i in range(16, len(msg)-(self.graph_erase_len*4+16), 4)]
            header = int(msg[1:2])
            if self.is_fft:
                fourier_transform = np.fft.rfft(np.array(data))
                abs_fourier_transform = np.abs(fourier_transform)
                power_spectrum = np.square(abs_fourier_transform)
                max_f = np.argmax(power_spectrum)
                max_val = power_spectrum[max_f]
                # power_spectrum /= max_val
                frequency = np.linspace(0, self.fsamp/2, len(power_spectrum))
                self.graph.annotate(f'{np.round((self.fsamp/2)/len(frequency)*max_f)} Hz', xy=(max_f, max_val), xytext=(np.max(frequency)//10*8, max_val))
                self.graph.plot(frequency, power_spectrum)
            else:
                self.graph.plot(data)
            self.canvas.draw()
        self.after(int(500000/(self.fsamp)), self.draw_ddc)

    def send_btn_command(self) -> None:
        try:
            conf = [self.checkInput(int(self.d300e.get()), '300'),
                    self.checkInput(int(self.d301e.get()), '301'),
                    0,  # NCO Sync mask
                    self.checkInput(self.getNCO(int(self.d303e.get())), '303'),
                    self.checkInput(int(self.d304e.get()), '304'),
                    self.checkInput(int(self.d305e.get()), '305'),
                    self.checkInput(int(self.d306e.get())-1, '306'),
                    self.checkInput(int(self.d307e.get()), '307'),
                    self.checkInput(int(self.d308e.get())-1, '308'),
                    self.checkInput(int(self.d309e.get()), '309'),
                    self.checkInput(int(self.d30Ae.get())-1, '30A'),
                    self.checkInput(int(self.d30Be.get()), '30B'),
                    self.checkInput(int(self.d30Ce.get())-1, '30C')]
        except ValueError as e:
            messagebox.showerror('Error', 'Wrong input!')
            return
        self.is_graph = False
        self.udp_send('L'.encode())
        data_to_send = ''
        for i, item in enumerate(conf):
            ind = f'{i}'.zfill(2)
            data_to_send += (f'A{ind}B' + str(item).zfill(12))
        self.udp_send(data_to_send.encode())
        self.total_decimation = (conf[6]+1) * (conf[8]+1) * (conf[10]+1)
        self.fsamp = int(self.fclock / self.total_decimation)
        self.udp_send('L'.encode())
        self.is_graph = True

    def udp_send(self, data: bytes) -> None:
        self.UDP_server_soc.sendto(data, (self.DDC_IP, self.DDC_PORT))

    def udp_receive(self):
        if self.is_con:
            bytesAddressPair = self.UDP_server_soc.recv(self.BUFFER_SIZE)
            return bytesAddressPair.hex()
        return

    def connect_ddc(self) -> None:
        self.UDP_server_soc.bind((self.PC_IP, self.PC_PORT))
        self.con_btn['state'] = DISABLED
        self.is_con = True

    def getNCO(self, value: int) -> int:
        return round(2**32 * (value / self.fclock))

    def graph_btn_command(self):
        self.is_fft = not self.is_fft
        if self.is_fft:
            self.graph_btn['text'] = 'RAW'
        else:
            self.graph_btn['text'] = 'FFT'

    def graph_nav_btn_command(self):
        try:
            val = int(self.graph_nav_e.get())
        except ValueError:
            messagebox.showerror('Error', 'Wrong input. Please insert number between 1 to 500!')
            return
        if val > 500:
            messagebox.showwarning('Warning', 'Input value exceeds maximum sample count!')
            self.graph_erase_len = 0
            return
        self.graph_erase_len = 500 - val

    def checkInput(self, inpt, reg):
        if inpt < 0:
            messagebox.showwarning('Warning', f'{reg} value can\'t ve lower than 0')
            return 0
        else:
            return inpt

    @staticmethod
    def hex2int(hexval):
        bits = 16
        val = int(hexval, 16)
        if val & (1 << (bits-1)):
            val -= 1 << bits
        return val


DDC()
