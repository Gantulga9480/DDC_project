import socket
import numpy as np
from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from DDC_REGS import *
import select
import json


class DDC(Tk):

    BUFFER_SIZE = 1024

    def __init__(self, screenName=None, baseName=None,
                 useTk=1, sync=0, use=None) -> None:
        super().__init__(screenName=screenName, baseName=baseName,
                         useTk=useTk, sync=sync, use=use)

        self.host_name = socket.gethostname()
        self.host_ips = socket.gethostbyname_ex(self.host_name)[2]
        self.no_data_warn = False
        self.PC_IP = StringVar(self)
        self.PC_PORT = ''
        self.DDC_IP = ''
        self.DDC_PORT = ''

        self.REGS_LAST = {
            '302': D302_DCT['DEFAULT'],
            '303': D303_DCT['DEFAULT'],
            '304': D304_DCT['DEFAULT'],
            '305': D305_DCT['DEFAULT'],
            '306': D306_DCT['DEFAULT'],
            '307': D307_DCT['DEFAULT'],
            '308': D308_DCT['DEFAULT'],
            '309': D309_DCT['DEFAULT'],
            '30A': D30A_DCT['DEFAULT'],
            '30B': D30B_DCT['DEFAULT'],
            '30C': D30C_DCT['DEFAULT'],
        }

        self.d300_var = StringVar(self)
        self.d301_var = StringVar(self)
        self.d305_expinv_var = BooleanVar(self)
        self.d309_uBmode_var = BooleanVar(self)
        self.surpass_warning = BooleanVar(self, value=False)

        self.UDP_server_soc = None

        self.title('DDC Utility')
        self.resizable(False, False)

        self.d300l = ttk.Label(self, text='DDC MODE            ')
        self.d301l = ttk.Label(self, text='NCO MODE            ')
        self.d302l = ttk.Label(self, text='NCO SYNC MASK       ')
        self.d303l = ttk.Label(self, text='NCO FREQUENCY  (KHz)')
        self.d304l = ttk.Label(self, text='NCO PHASE OFFSET    ')
        self.d305l = ttk.Label(self, text='CIC2 SCALE          ')
        self.d306l = ttk.Label(self, text='CIC2 DECIMATION (-1)')
        self.d307l = ttk.Label(self, text='CIC5 SCALE          ')
        self.d308l = ttk.Label(self, text='CIC5 DECIMATION (-1)')
        self.d309l = ttk.Label(self, text='RCF SCALE           ')
        self.d30Al = ttk.Label(self, text='RCF DECIMATION  (-1)')
        self.d30Bl = ttk.Label(self, text='RCF ADDRESS OFFSET  ')
        self.d30Cl = ttk.Label(self, text='RCF FILTER TAPS (-1)')

        self.d300m = ttk.Combobox(self,
                                  value=D300_OPT,
                                  textvariable=self.d300_var)
        self.d300m.current(0)
        self.d300m.config(state="readonly", width=22)
        self.d300m.bind("<<ComboboxSelected>>")

        self.d301m = ttk.Combobox(self,
                                  value=D301_OPT,
                                  textvariable=self.d301_var)
        self.d301m.current(0)
        self.d301m.config(state="readonly", width=22)
        self.d301m.bind("<<ComboboxSelected>>")

        self.d302e = ttk.Entry(self, width=25)
        self.d303e = ttk.Entry(self, width=25)
        self.d304e = ttk.Entry(self, width=25)
        self.d305e = ttk.Entry(self, width=25)
        self.d306e = ttk.Entry(self, width=25)
        self.d307e = ttk.Entry(self, width=25)
        self.d308e = ttk.Entry(self, width=25)
        self.d309e = ttk.Entry(self, width=25)
        self.d30Ae = ttk.Entry(self, width=25)
        self.d30Be = ttk.Entry(self, width=25)
        self.d30Ce = ttk.Entry(self, width=25)

        self.ddcClock_l = ttk.Label(self, text='DDC Fc (MHz)')
        self.ddcClock_e = ttk.Entry(self, width=25)
        self.ddcClock_e.insert(END, '30')
        self.config(bg="#FFFFFF")

        self.ip_frame = ttk.Frame(self)
        self.ip_style = ttk.Style(self.ip_frame)
        self.ip_style.configure('TFrame', background='white')

        self.pcip_l = ttk.Label(self.ip_frame, text='PC  IP:PORT   ')
        self.pcip_style = ttk.Style(self.pcip_l)
        self.pcip_style.configure('TLabel', background='white')
        self.ddcip_l = ttk.Label(self.ip_frame,
                                 text='DDC IP:PORT               ')

        self.pcip_m = ttk.Combobox(self.ip_frame,
                                   value=self.host_ips,
                                   textvariable=self.PC_IP)
        self.pcip_m.current(0)
        self.pcip_m.config(state="readonly", width=15)
        self.pcip_m.bind("<<ComboboxSelected>>")

        self.pcport_e = ttk.Entry(self.ip_frame, width=7)
        self.ddcip_e = ttk.Entry(self.ip_frame, width=18)
        self.ddcport_e = ttk.Entry(self.ip_frame, width=7)

        self.opt_frame = ttk.Frame(self)

        self.d305_expoff_l = ttk.Label(self.opt_frame,
                                       text='INPUT ExpOff (optional)')
        self.d305_expinv_l = ttk.Label(self.opt_frame, text='INPUT ExpInv')
        self.d309_uBmode_l = ttk.Label(self.opt_frame, text='UNIQUE B MODE')

        self.d305_expinv_c = ttk.Checkbutton(self.opt_frame,
                                             variable=self.d305_expinv_var)
        self.d305_expinv_style = ttk.Style(self.d305_expinv_c)
        self.d305_expinv_style.configure('TCheckbutton', background='white')
        self.d309_uBmode_c = ttk.Checkbutton(self.opt_frame,
                                             variable=self.d309_uBmode_var)

        self.d305_expoff_e = ttk.Entry(self.opt_frame, width=25)

        self.btn_frame = ttk.Frame(self)

        self.con_btn = ttk.Button(self.btn_frame, text="Connect",
                                  command=self.connect_ddc)
        self.con_btn_style = ttk.Style(self.con_btn)
        self.con_btn_style.configure('TButton', background='white')
        self.send_btn = ttk.Button(self.btn_frame, text="Write",
                                   command=self.send_btn_command,
                                   state=DISABLED)
        self.read_btn = ttk.Button(self.btn_frame, text="Read",
                                   command=self.read_btn_command,
                                   state=DISABLED)

        self.fig = plt.figure()
        self.graph = plt.subplot()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.graph_btn = ttk.Button(self, text="FFT",
                                    command=self.graph_btn_command)

        self.graph_nav_frame = ttk.Frame(self)
        self.graph_nav_l = ttk.Label(self.graph_nav_frame, text='Set interval (max = 250)')
        self.graph_nav_e = ttk.Entry(self.graph_nav_frame, width=10)
        self.graph_nav_e.bind('<Return>', self.graph_nav_btn_command)

        self.opt_frame.grid(row=0, column=4, columnspan=3)
        self.d305_expoff_l.grid(row=0, column=0, padx=1)
        self.d305_expoff_e.grid(row=0, column=1, padx=10)
        self.d305_expinv_l.grid(row=0, column=2, padx=1)
        self.d305_expinv_c.grid(row=0, column=3, padx=10)
        self.d309_uBmode_l.grid(row=0, column=4, padx=1)
        self.d309_uBmode_c.grid(row=0, column=5, padx=10)

        self.canvas.get_tk_widget().grid(row=1, column=4,
                                         rowspan=14, columnspan=3)
        self.graph_nav_frame.grid(row=15,column=4)
        self.graph_nav_l.grid(row=0, column=0, sticky=NS)
        self.graph_nav_e.grid(row=0, column=1, sticky=NS)
        self.graph_btn.grid(row=15, column=5, sticky=NS)

        self.d300l.grid(row=0, column=0, sticky=W)
        self.d300m.grid(row=0, column=1)
        self.d301l.grid(row=1, column=0, sticky=W)
        self.d301m.grid(row=1, column=1)
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

        self.ddcClock_l.grid(row=13, column=0)
        self.ddcClock_e.grid(row=13, column=1)

        self.ip_frame.grid(row=14, column=0, columnspan=2, sticky=EW)
        self.pcip_l.grid(row=0, column=0, sticky=W)
        self.pcip_m.grid(row=0, column=1)
        self.pcport_e.grid(row=0, column=2)
        self.ddcip_l.grid(row=1, column=0, sticky=W)
        self.ddcip_e.grid(row=1, column=1)
        self.ddcport_e.grid(row=1, column=2)

        self.btn_frame.grid(row=15, column=0, columnspan=2)
        self.con_btn.grid(row=0, column=0, padx=3)
        self.send_btn.grid(row=0, column=2, padx=3)
        self.read_btn.grid(row=0, column=1, padx=3)

        try:
            with open('conf.json', 'r') as file:
                self.REGS_LAST = json.load(file)
            self.d302e.insert(END, str(self.REGS_LAST['302']))
            self.d303e.insert(END, str(self.REGS_LAST['303']))
            self.d304e.insert(END, str(self.REGS_LAST['304']))
            self.d305e.insert(END, str(self.REGS_LAST['305']))
            self.d306e.insert(END, str(self.REGS_LAST['306']+1))
            self.d307e.insert(END, str(self.REGS_LAST['307']))
            self.d308e.insert(END, str(self.REGS_LAST['308']+1))
            self.d309e.insert(END, str(self.REGS_LAST['309']))
            self.d30Ae.insert(END, str(self.REGS_LAST['30A']+1))
            self.d30Be.insert(END, str(self.REGS_LAST['30B']))
            self.d30Ce.insert(END, str(self.REGS_LAST['30C']+1))
        except FileNotFoundError:
            with open('conf.json', 'w') as file:
                json.dump(REGS_DEFAULT, file)
            self.d302e.insert(END, str(REGS_DEFAULT['302']))
            self.d303e.insert(END, str(REGS_DEFAULT['303']))
            self.d304e.insert(END, str(REGS_DEFAULT['304']))
            self.d305e.insert(END, str(REGS_DEFAULT['305']))
            self.d306e.insert(END, str(REGS_DEFAULT['306']+1))
            self.d307e.insert(END, str(REGS_DEFAULT['307']))
            self.d308e.insert(END, str(REGS_DEFAULT['308']+1))
            self.d309e.insert(END, str(REGS_DEFAULT['309']))
            self.d30Ae.insert(END, str(REGS_DEFAULT['30A']+1))
            self.d30Be.insert(END, str(REGS_DEFAULT['30B']))
            self.d30Ce.insert(END, str(REGS_DEFAULT['30C']+1))

        self.total_decimation = 1
        self.total_decimation = int(self.d306e.get()) * int(self.d308e.get()) \
            * int(self.d30Ae.get())

        self.fclock = 30 * 10**6
        self.fsamp = int(self.fclock / self.total_decimation)

        self.is_con = False
        self.is_fft = False
        self.is_graph = True

        self.graph_erase_len = 0

        self.draw_ddc()
        self.mainloop()

    def draw_ddc(self):
        if self.is_con and self.is_graph:
            self.graph.cla()
            msg = self.udp_receive(self.BUFFER_SIZE)
            if msg:
                i_data = [self.hex2int(msg[i+2:i+4] + msg[i:i+2]) for i in range(8, len(msg)-(self.graph_erase_len*4+8), 8)]
                q_data = [self.hex2int(msg[i+2:i+4] + msg[i:i+2]) for i in range(12, len(msg)-(self.graph_erase_len*4+8), 8)]
                if len(i_data) > 0:
                    if self.is_fft:
                        i_fft = np.fft.rfft(np.array(i_data))
                        q_fft = np.fft.rfft(np.array(q_data))
                        I_fft = np.square(np.abs(i_fft))
                        Q_fft = np.square(np.abs(q_fft))
                        imax_f = np.argmax(I_fft)
                        qmax_f = np.argmax(Q_fft)
                        I_f = np.linspace(0, self.fsamp/2, len(I_fft))
                        Q_f = np.linspace(0, self.fsamp/2, len(Q_fft))
                        max_val = max(I_fft[imax_f], Q_fft[qmax_f])
                        self.graph.annotate(f'I {int(np.round((self.fsamp/2)/len(I_f)*imax_f))} Hz', xy=(imax_f, max_val), xytext=(np.max(I_f)//10*6, max_val))
                        self.graph.annotate(f'Q {int(np.round((self.fsamp/2)/len(Q_f)*qmax_f))} Hz', xy=(qmax_f, max_val), xytext=(np.max(I_f)//10*8, max_val))
                        self.graph.plot(I_f, I_fft, 'r')
                        self.graph.plot(Q_f, Q_fft)
                        self.graph.legend(['I', 'Q'], loc='lower right')
                    else:
                        self.graph.plot(i_data, 'r')
                        self.graph.plot(q_data)
                        self.graph.legend(['I', 'Q'], loc='upper right')
                    if self.no_data_warn:
                        self.no_data_warn = False
            else:
                if not self.no_data_warn:
                    self.throw_warning('No data available at socket!')
                    self.no_data_warn = True
        self.canvas.draw()
        self.after(int(500000/(self.fsamp)), self.draw_ddc)

    def read_btn_command(self) -> None:
        """ Depricated """
        cmd = 'READ_DDC'
        res = None
        self.udp_send('L'.encode())
        self.udp_send(cmd.encode())
        # while True:
        #     res = self.udp_receive(150)
        #     if res[0:2] == '52':
        #         break
        # TODO handle res
        self.udp_send('L'.encode())

    def send_btn_command(self) -> None:
        try:
            self.setDDCFs()
            conf = [self.checkInput(self.d300m.get(), '300'),
                    self.checkInput(self.d301m.get(), '301'),
                    self.checkInput(self.d302e.get(), '302'),
                    self.checkInput(self.d303e.get(), '303'),
                    self.checkInput(self.d304e.get(), '304'),
                    self.checkInput(self.d305e.get(), '305'),
                    self.checkInput(self.d306e.get(), '306'),
                    self.checkInput(self.d307e.get(), '307'),
                    self.checkInput(self.d308e.get(), '308'),
                    self.checkInput(self.d309e.get(), '309'),
                    self.checkInput(self.d30Ae.get(), '30A'),
                    self.checkInput(self.d30Be.get(), '30B'),
                    self.checkInput(self.d30Ce.get(), '30C')]
        except ValueError as e:
            messagebox.showerror('Error', 'Wrong input!')
            return
        self.total_decimation = (conf[6]+1) * (conf[8]+1) * (conf[10]+1)
        self.fsamp = self.fclock // self.total_decimation

        if self.fclock > 30 * 10**6:
            messagebox.showwarning('Warning', 'DDC Fc is too high. DMA '
                                              'under run may occure!')
        if self.total_decimation < 4:
            messagebox.showwarning('Warning', 'Total Decimation is too low. '
                                              'DDC may not work!')

        data_to_send = ''
        for i, item in enumerate(conf):
            ind = f'{i}'.zfill(2)
            data_to_send += (f'A{ind}B' + str(item).zfill(12))
        self.is_graph = False
        self.udp_send('L'.encode())
        self.udp_send(data_to_send.encode())
        self.udp_send('L'.encode())
        self.is_graph = True
        conf.pop(0)
        conf.pop(0)
        self.REGS_LAST['302'] = conf[0]
        self.REGS_LAST['303'] = int(self.d303e.get())
        self.REGS_LAST['304'] = conf[2]
        self.REGS_LAST['305'] = conf[3]
        self.REGS_LAST['306'] = conf[4]
        self.REGS_LAST['307'] = conf[5]
        self.REGS_LAST['308'] = conf[6]
        self.REGS_LAST['309'] = conf[7]
        self.REGS_LAST['30A'] = conf[8]
        self.REGS_LAST['30B'] = conf[9]
        self.REGS_LAST['30C'] = conf[10]
        with open('conf.json', 'w') as file:
            json.dump(self.REGS_LAST, file)

    def setDDCFs(self):
        try:
            clk = int(self.ddcClock_e.get()) * 1_000_000
            if clk:
                self.fclock = clk
        except ValueError:
            messagebox.showerror('Error', 'Enter valid DDC Fc value in MHz')
            raise ValueError

    def checkInput(self, inpt: str, reg: str):
        if reg == '300':
            return D300_DCT[inpt]
        elif reg == '301':
            return D301_DCT[inpt]
        elif reg == '302':
            val = int(inpt)
            if REGS_MIN[reg] <= val <= REGS_MAX[reg]:
                return val
            else:
                self.throw_warning('NCO Sync mask using default '
                                   f'value of {REGS_DEFAULT[reg]}')
                return REGS_DEFAULT[reg]
        elif reg == '303':
            val = self.getNCO(int(inpt))
            if REGS_MIN[reg] <= val <= REGS_MAX[reg]:
                return val
            else:
                self.throw_warning('NCO Frequency using default '
                                   f'value of {REGS_DEFAULT[reg]}')
                return self.getNCO(REGS_DEFAULT[reg])
        elif reg == '304':
            val = int(inpt)
            if REGS_MIN[reg] <= val <= REGS_MAX[reg]:
                return val
            else:
                self.throw_warning('NCO Phase offset using default '
                                   f'value of {REGS_DEFAULT[reg]}')
                return REGS_DEFAULT[reg]
        elif reg == '305':
            val = int(inpt)
            if REGS_MIN[reg] <= val <= REGS_MAX[reg]:
                exp_val = self.d305_expoff_e.get()
                if exp_val:
                    exp_val = int(exp_val)
                    if 0 > exp_val or exp_val > 7:
                        self.throw_warning('Wrong CIC2/INPUT ExpOffset '
                                           'value. ExpOffset set to 0.')
                        exp_val = 0
                    else:
                        exp_val = exp_val << 5
                else:
                    exp_val = 0
                if self.d305_expinv_var.get():
                    return val + 16 + exp_val
                return val + exp_val
            else:
                self.throw_warning('CIC2 Scale using default '
                                   f'value of {REGS_DEFAULT[reg]}')
                return REGS_DEFAULT[reg]
        elif reg == '306':
            val = int(inpt) - 1
            if REGS_MIN[reg] <= val <= REGS_MAX[reg]:
                return val
            else:
                self.throw_warning('CIC2 Decimation using default '
                                   f'value of {REGS_DEFAULT[reg]}')
                return REGS_DEFAULT[reg]
        elif reg == '307':
            val = int(inpt)
            if REGS_MIN[reg] <= val <= REGS_MAX[reg]:
                return val
            else:
                self.throw_warning('CIC5 Scale using default '
                                   f'value of {REGS_DEFAULT[reg]}')
                return REGS_DEFAULT[reg]
        elif reg == '308':
            val = int(inpt) - 1
            if REGS_MIN[reg] <= val <= REGS_MAX[reg]:
                return val
            else:
                self.throw_warning('CIC5 Decimation using default '
                                   f'value of {REGS_DEFAULT[reg]}')
                return REGS_DEFAULT[reg]
        elif reg == '309':
            val = int(inpt)
            if REGS_MIN[reg] <= val <= REGS_MAX[reg]:
                if self.d309_uBmode_var.get():
                    return val + 8
                return val
            else:
                self.throw_warning('RCF Scale using default '
                                   f'value of {REGS_DEFAULT[reg]}')
                return REGS_DEFAULT[reg]
        elif reg == '30A':
            val = int(inpt) - 1
            mode = self.d300_var.get()
            dec1 = int(self.d306e.get())
            dec2 = int(self.d308e.get())
            if REGS_MIN[reg] <= val <= REGS_MAX[reg]:
                self.total_decimation = dec1 * dec2 * (val + 1)
                if mode == D300_OPT[1] or mode == D300_OPT[4]:
                    D30C_DCT['MAX'] = min(255, self.total_decimation // 2)
                else:
                    D30C_DCT['MAX'] = min(255, self.total_decimation)
                return val
            else:
                self.total_decimation = dec1 * dec2 * (REGS_DEFAULT[reg] + 1)
                if mode == D300_OPT[1] or mode == D300_OPT[4]:
                    D30C_DCT['MAX'] = min((dec1 * dec2) // 2 - 1, 255)
                else:
                    D30C_DCT['MAX'] = min(dec1 * dec2 - 1, 255)
                self.throw_warning('RCF Decimation using default '
                                   f'value of {REGS_DEFAULT[reg]}')
                return REGS_DEFAULT[reg]
        elif reg == '30B':
            val = int(inpt)
            if REGS_MIN[reg] <= val <= REGS_MAX[reg]:
                return val
            else:
                self.throw_warning('RCF Addres offset using default '
                                   f'value of {REGS_DEFAULT[reg]}')
                return REGS_DEFAULT[reg]
        elif reg == '30C':
            val = int(inpt) - 1
            if REGS_MIN[reg] <= val <= REGS_MAX[reg]:
                return val
            else:
                self.throw_warning('Please check Decimation rates. '
                                   'RCF FILRER Taps using default '
                                   f'value of {REGS_DEFAULT[reg]}')
                return REGS_DEFAULT[reg]

    def connect_ddc(self) -> None:
        if not self.is_con:
            self.UDP_server_soc = socket.socket(family=socket.AF_INET,
                                                type=socket.SOCK_DGRAM)
            try:
                self.UDP_server_soc.bind((self.PC_IP.get(),
                                          int(self.pcport_e.get())))
                self.con_btn['text'] = 'Disconnect'
                self.send_btn['state'] = ACTIVE
                self.is_con = True
            except OSError as e:
                if str(e).split(' ')[1] == '10048]':
                    messagebox.showerror('Error', 'Can\'t listen on port '
                                         f'{self.pcport_e.get()}')
            except Exception:
                messagebox.showerror('Error', 'Please insert valid IP/PORT')
        else:
            self.UDP_server_soc.shutdown(socket.SHUT_RDWR)
            self.UDP_server_soc.close()
            self.con_btn['text'] = 'Connect'
            self.send_btn['state'] = DISABLED
            self.is_con = False
            self.no_data_warn = False

    def getNCO(self, value: int) -> int:
        return round(2**32 * ((value * 1000) / self.fclock))

    def udp_send(self, data: bytes) -> None:
        if self.is_con:
            try:
                self.UDP_server_soc.sendto(data, (self.ddcip_e.get(),
                                                  int(self.ddcport_e.get())))
            except Exception:
                # TODO
                messagebox.showerror('Error', 'UDP SEND ERROR!')

    def udp_receive(self, size):
        if self.is_con:
            ready, _, _ = select.select([self.UDP_server_soc], [], [], 0.05)
            if ready:
                bytesAddressPair = self.UDP_server_soc.recv(size)
                return bytesAddressPair.hex()

    def graph_nav_btn_command(self, event):
        try:
            val = int(self.graph_nav_e.get()) * 2
        except ValueError:
            self.throw_warning('Wrong input. Please insert '
                               'number between 5 to 250!')
            return
        if val > 500:
            self.throw_warning('The input value exceeds maximum sample count!')
            self.graph_erase_len = 0
            return
        elif val < 5:
            self.throw_warning('The input value shouldn\'t be lower than 5!')
            self.graph_erase_len = 0
            return
        self.graph_erase_len = 500 - val

    def graph_btn_command(self):
        self.is_fft = not self.is_fft
        if self.is_fft:
            self.graph_btn['text'] = 'RAW'
        else:
            self.graph_btn['text'] = 'FFT'

    def throw_warning(self, msg):
        if not self.surpass_warning.get():
            messagebox.showwarning('Warning', msg)

    @staticmethod
    def hex2int(hexval):
        bits = 16
        val = int(hexval, 16)
        if val & (1 << (bits-1)):
            val -= 1 << bits
        return val


DDC()
