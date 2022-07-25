import socket
import numpy as np
from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from DDC_REGS import *
import select
import json
from low_level_delay import delay_ms


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
        self.dfir_var = BooleanVar(self, value=False)
        self.pmod_var = BooleanVar(self, value=True)

        self.UDP_server_soc = None

        self.title('DDC Utility')
        self.resizable(False, False)

        # -------------------------------------------------------------DDC CONF
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
        self.dfirl = ttk.Label(self, text='ENABLE RCF FIR      ')

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

        self.dfirc = ttk.Checkbutton(self, variable=self.dfir_var)

        self.ddcClock_l = ttk.Label(self, text='DDC Fc (MHz)')
        self.ddcClock_e = ttk.Entry(self, width=25)
        self.ddcClock_e.insert(END, '30')
        self.config(bg="#FFFFFF")

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
        self.dfirl.grid(row=13, column=0, sticky=W)
        self.dfirc.grid(row=13, column=1)

        self.ddcClock_l.grid(row=14, column=0)
        self.ddcClock_e.grid(row=14, column=1)

        # --------------------------------------------------------------IP/PORT
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

        self.ip_frame.grid(row=15, column=0, columnspan=2, sticky=EW)
        self.pcip_l.grid(row=0, column=0, sticky=W)
        self.pcip_m.grid(row=0, column=1)
        self.pcport_e.grid(row=0, column=2)
        self.ddcip_l.grid(row=1, column=0, sticky=W)
        self.ddcip_e.grid(row=1, column=1)
        self.ddcport_e.grid(row=1, column=2)

        # ---------------------------------------------------------------OPTION
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

        self.pmod_sync_l = ttk.Label(self.opt_frame, text='Pmod')
        self.pmod_sync_c = ttk.Checkbutton(self.opt_frame,
                                           variable=self.pmod_var,
                                           command=self.pmod_c_command)
        self.d305_expoff_e = ttk.Entry(self.opt_frame, width=25)

        self.opt_frame.grid(row=0, column=2)
        self.d305_expoff_l.grid(row=0, column=0, padx=1)
        self.d305_expoff_e.grid(row=0, column=1)
        self.d305_expinv_l.grid(row=0, column=2, padx=1)
        self.d305_expinv_c.grid(row=0, column=3)
        self.d309_uBmode_l.grid(row=0, column=4, padx=1)
        self.d309_uBmode_c.grid(row=0, column=5)
        self.pmod_sync_l.grid(row=0, column=6)
        self.pmod_sync_c.grid(row=0, column=7)

        # ---------------------------------------------------------------BUTTON
        self.btn_frame = ttk.Frame(self)
        self.con_btn = ttk.Button(self.btn_frame, text="Connect",
                                  command=self.connect_ddc)
        self.send_btn = ttk.Button(self.btn_frame, text="Write",
                                   command=self.send_btn_command,
                                   state=DISABLED)
        self.read_btn = ttk.Button(self.btn_frame, text="Read",
                                   command=self.read_btn_command,
                                   state=DISABLED)
        self.con_btn_style = ttk.Style(self.con_btn)
        self.con_btn_style.configure('TButton', background='white')

        self.btn_frame.grid(row=16, column=0, columnspan=2)
        self.con_btn.grid(row=0, column=0, padx=3)
        self.send_btn.grid(row=0, column=2, padx=3)
        self.read_btn.grid(row=0, column=1, padx=3)

        # ---------------------------------------------------------------FIGURE
        self.fig = plt.figure()
        self.graph = plt.subplot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(row=1, column=2,
                                         rowspan=15)

        # ------------------------------------------------------------GRAPH/NAV
        self.graph_nav_frame = ttk.Frame(self)
        self.graph_btn = ttk.Button(self.graph_nav_frame, text="FFT",
                                    command=self.graph_btn_command)
        self.graph_nav_x_l = ttk.Label(self.graph_nav_frame,
                                       text='Set X')
        self.graph_nav_x_e = ttk.Entry(self.graph_nav_frame, width=10)
        self.graph_nav_x_e.bind('<Return>', self.graph_nav_x_btn_command)
        self.graph_nav_y_l = ttk.Label(self.graph_nav_frame,
                                       text='Set Y')
        self.graph_nav_y_e = ttk.Entry(self.graph_nav_frame, width=10)
        self.graph_nav_y_e.bind('<Return>', self.graph_nav_y_btn_command)

        self.graph_nav_frame.grid(row=16, column=2)
        self.graph_nav_x_l.grid(row=0, column=0)
        self.graph_nav_x_e.grid(row=0, column=1, padx=10)
        self.graph_nav_y_l.grid(row=0, column=2)
        self.graph_nav_y_e.grid(row=0, column=3, padx=10)
        self.graph_btn.grid(row=0, column=4, padx=20)
        self.btn = ttk.Button(self)
        # self.btn.grid(row=17, column=2, ipadx=450)

        # ----------------------------------------------------------------CODER
        # self.coder_power = False
        # self.coder_start = False
        # self.coder_trigger = False
        # self.channels = ['Channel 1', 'Channel 2']
        # self.channels_var = StringVar()
        # self.freqs = ['150', '151', '152', '153', '154', '155', '156', '157',
        #               '158', '159', '160', '161', '162', '163', '164', '165',
        #               '166', '167', '168', '169', '170']
        # self.freqs_var = StringVar()
        # self.chs = ['1', '2', '3', '4', '5', '6', '7', '8']
        # self.ch1_var = StringVar()
        # self.ch2_var = StringVar()

        # style = ttk.Style()
        # style.configure('TLabelframe', background='SystemWindow')
        # style.configure('TLabelframe.Label', background='SystemWindow')

        # self.coder_ch_l = ttk.Label(self, text='CHANNEL')
        # self.coder_ch_l.grid(row=1, column=3, sticky=W)
        # self.coder_code_ch = ttk.Combobox(self,
        #                                   value=self.channels,
        #                                   textvariable=self.channels_var)
        # self.coder_code_ch.current(0)
        # self.coder_code_ch.config(state="readonly", width=15)
        # self.coder_code_ch.bind("<<ComboboxSelected>>")
        # self.coder_code_ch.grid(row=1, column=4)
        # self.coder_ch_f = ttk.Label(self, text='FREQUENCY')
        # self.coder_ch_f.grid(row=5, column=3, sticky=W)
        # self.coder_code_fq = ttk.Combobox(self,
        #                                   value=self.freqs,
        #                                   textvariable=self.freqs_var)
        # self.coder_code_fq.current(0)
        # self.coder_code_fq.config(state="readonly", width=15)
        # self.coder_code_fq.bind("<<ComboboxSelected>>")
        # self.coder_code_fq.grid(row=5, column=4)
        # self.coder_code_fq_btn = ttk.Button(self, text="Set frequency",
        #                                     command=self.coder_set_freq_cmd)
        # self.coder_code_fq_btn.grid(row=6, column=3, columnspan=2)

        # self.coder_ch_ch1_l = ttk.Label(self, text='ENTRY 1')
        # self.coder_ch_ch1_l.grid(row=10, column=3, sticky=W)
        # self.coder_code1 = ttk.Combobox(self,
        #                                 value=self.chs,
        #                                 textvariable=self.ch1_var)
        # self.coder_code1.current(0)
        # self.coder_code1.config(state="readonly", width=15)
        # self.coder_code1.bind("<<ComboboxSelected>>")
        # self.coder_code1.grid(row=10, column=4)

        # self.coder_ch_ch2_l = ttk.Label(self, text='ENTRY 2')
        # self.coder_ch_ch2_l.grid(row=11, column=3, sticky=W)
        # self.coder_code2 = ttk.Combobox(self,
        #                                 value=self.chs,
        #                                 textvariable=self.ch2_var)
        # self.coder_code2.current(0)
        # self.coder_code2.config(state="readonly", width=15)
        # self.coder_code2.bind("<<ComboboxSelected>>")
        # self.coder_code2.grid(row=11, column=4)
        # self.coder_freq_btn = ttk.Button(self, text="Set channel",
        #                                  command=self.coder_set_channel_cmd)
        # self.coder_freq_btn.grid(row=12, column=3, columnspan=2)

        # self.coder_btn_frame = ttk.Frame(self)
        # self.coder_btn_frame.grid(row=16, column=3, columnspan=2)
        # self.coder_power_btn = ttk.Button(self.coder_btn_frame,
        #                                   text='POWER ON',
        #                                   command=self.coder_power_btn_cmd)
        # self.coder_start_btn = ttk.Button(self.coder_btn_frame,
        #                                   text='START',
        #                                   command=self.coder_start_btn_cmd)
        # self.coder_trigger_btn = ttk.Button(self.coder_btn_frame,
        #                                     text='TRIGGER ON',
        #                                     command=self.coder_trigger_btn_cmd)

        # self.coder_power_btn.grid(row=0, column=0)
        # self.coder_start_btn.grid(row=0, column=1)
        # self.coder_trigger_btn.grid(row=0, column=2)

        # ---------------------------------------------------------------------
        self.pcport_e.insert(END, '10')
        self.ddcip_e.insert(END, '10.3.4.123')
        self.ddcport_e.insert(END, '11')

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

        self.graph_len = 1000
        self.graph_len_max = self.graph_len
        self.graph_scale = 35000
        self.fft_last_scale = 5000

        self.prev_header = ''

        self.draw_ddc()
        self.mainloop()

    def draw_ddc(self):
        if self.is_con and self.is_graph:
            msg = self.receive_packet()
            if msg:
                self.graph.cla()
                i_data = [self.hex2int(msg[i+2:i+4] + msg[i:i+2])
                          for i in
                          range(0, len(msg), 4)]
                if self.is_fft:
                    i_fft = np.fft.rfft(np.array(i_data))
                    I_fft = np.abs(i_fft/len(i_data))
                    imax_f = np.argmax(I_fft)
                    I_f = np.linspace(0, self.fsamp/2, len(I_fft))
                    max_val = I_fft[imax_f]
                    fi = round(np.round((self.fsamp/2)/len(I_f)*imax_f)
                               / 1000, 2)
                    if self.fft_last_scale < max_val:
                        self.fft_last_scale = max_val+1000
                    else:
                        if self.fft_last_scale / (max_val + 1) > 2:
                            while True:
                                ratio = self.fft_last_scale / (max_val + 1)
                                if ratio > 2:
                                    self.fft_last_scale //= 2
                                else:
                                    break
                    self.graph.annotate(f'I - {fi} KHz',
                                        xy=(0, 0),
                                        xytext=(np.max(I_f)//2,
                                                self.fft_last_scale))
                    self.graph.plot(I_f, I_fft, 'r')
                    plt.ylim(0, (self.fft_last_scale+1))
                    self.graph.legend(['I', 'Q'], loc='lower right')
                else:
                    imx = max(i_data)
                    self.graph.annotate(f'I - {imx}',
                                        xy=(0, 0),
                                        xytext=(self.graph_len//10*6,
                                                self.graph_scale))
                    self.graph.plot(i_data, 'r')
                    plt.ylim(-self.graph_scale, self.graph_scale)
                    plt.xlim(0, self.graph_len)
                    self.graph.legend(['I'], loc='upper right')
        self.canvas.draw()
        self.after(int(1), self.draw_ddc)

    def read_btn_command(self) -> None:
        """ Depricated """
        cmd = 'R'
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
                    self.checkInput(self.d30Ce.get(), '30C'),
                    self.checkInput(str(self.dfir_var.get()), 'FIR')]
        except ValueError as e:
            messagebox.showerror('Error', 'Wrong input!')
            return
        self.total_decimation = (conf[6]+1) * (conf[8]+1) * (conf[10]+1)
        self.fsamp = self.fclock // self.total_decimation

        if self.fclock > 30 * 10**6:
            self.throw_warning('Warning', 'DDC Fc is too high. DMA '
                               'under run may occure!')
        if self.total_decimation < 4:
            self.throw_warning('Warning', 'Total Decimation is too low. '
                               'DMA may not work!')
        data_to_send = ''
        for i, item in enumerate(conf):
            ind = f'{i}'.zfill(2)
            data_to_send += (f'A{ind}B' + str(item).zfill(12))
        self.is_graph = False
        self.udp_send('L'.encode())
        self.udp_send(data_to_send.encode())
        delay_ms(100)
        self.udp_send('L'.encode())
        self.connect_ddc()
        delay_ms(10)
        self.connect_ddc()
        self.is_graph = True
        self.REGS_LAST['302'] = conf[2]
        self.REGS_LAST['303'] = int(self.d303e.get())
        self.REGS_LAST['304'] = conf[4]
        self.REGS_LAST['305'] = conf[5]
        self.REGS_LAST['306'] = conf[6]
        self.REGS_LAST['307'] = conf[7]
        self.REGS_LAST['308'] = conf[8]
        self.REGS_LAST['309'] = conf[9]
        self.REGS_LAST['30A'] = conf[10]
        self.REGS_LAST['30B'] = conf[11]
        self.REGS_LAST['30C'] = conf[12]
        with open('conf.json', 'w') as file:
            json.dump(self.REGS_LAST, file)

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
                self.throw_warning('RCF FILRER Taps using default '
                                   f'value of {REGS_DEFAULT[reg]}')
                return REGS_DEFAULT[reg]
        elif reg == 'FIR':
            if inpt == 'True':
                return 1
            else:
                return 0

    def connect_ddc(self) -> None:
        if not self.is_con:
            self.UDP_server_soc = socket.socket(family=socket.AF_INET,
                                                type=socket.SOCK_DGRAM)
            try:
                self.UDP_server_soc.bind((self.PC_IP.get(),
                                          int(self.pcport_e.get())))
            except OSError as e:
                if str(e).split(' ')[1] == '10048]':
                    messagebox.showerror('Error', 'Can\'t listen on port '
                                         f'{self.pcport_e.get()}')
                return
            except Exception:
                messagebox.showerror('Error', 'Please insert valid IP/PORT')
                return
            self.con_btn['text'] = 'Disconnect'
            self.send_btn['state'] = ACTIVE
            self.is_con = True
        else:
            self.UDP_server_soc.shutdown(socket.SHUT_RDWR)
            self.UDP_server_soc.close()
            self.con_btn['text'] = 'Connect'
            self.send_btn['state'] = DISABLED
            self.is_con = False

    def udp_send(self, data: bytes) -> None:
        try:
            self.UDP_server_soc.sendto(data, (self.ddcip_e.get(),
                                       int(self.ddcport_e.get())))
            return True
        except Exception:
            messagebox.showerror('Error', 'UDP SEND ERROR!')
            return False

    def udp_receive(self, size):
        ready, _, _ = select.select([self.UDP_server_soc], [], [], 0.01)
        if ready:
            msg = self.UDP_server_soc.recv(size).hex()
            return self.check_header(msg)

    def check_header(self, msg):
        if msg[:8] == '41424142':
            self.prev_header = '41424142'
            return msg[8:]
        elif msg[-8:] == '43444344':
            self.prev_header = '43444344'
            return msg[:-8]
        else:
            return msg

    def receive_packet(self):
        if self.pmod_var.get():
            msg1 = self.udp_receive(self.BUFFER_SIZE)
            if self.prev_header == '41424142':
                msg2 = self.udp_receive(self.BUFFER_SIZE)
                if self.prev_header == '43444344':
                    try:
                        msg = msg1 + msg2
                        return msg
                    except Exception:
                        pass
        else:
            msg1 = self.udp_receive(self.BUFFER_SIZE)
            if self.prev_header == '41424142':
                return msg1

    # ------------------------------------------------------- COMMAND CALLBACKS

    def coder_set_freq_cmd(self):
        if not self.coder_trigger and self.coder_start:
            if self.udp_send('L'.encode()):
                send_data = 'CF'
                ch = self.channels_var.get()
                if ch == self.channels[0]:
                    ind = str(self.freqs.index(self.freqs_var.get())).zfill(2)
                    send_data += '1' + ind
                elif ch == self.channels[1]:
                    ind = str(self.freqs.index(self.freqs_var.get())
                              + 21).zfill(2)
                    send_data += '2' + ind
                self.udp_send(send_data.encode())
                print(send_data)
                self.udp_send('L'.encode())
        else:
            if not self.coder_start:
                self.throw_error('Coder not started!')
            else:
                self.throw_error('Trigger mode ON!')

    def coder_set_channel_cmd(self):
        if not self.coder_trigger and self.coder_start:
            if self.udp_send('L'.encode()):
                send_data = 'CC'
                ch = self.channels_var.get()
                f1 = int(self.ch1_var.get())
                f2 = int(self.ch2_var.get())
                index = 0
                if ch == self.channels[1]:
                    index += 64
                index += ((f1-1)*8 + (f2-1))
                send_data += str(index).zfill(4)
                print(send_data)
                self.udp_send(send_data.encode())
                self.udp_send('L'.encode())
        else:
            if not self.coder_start:
                self.throw_error('Coder not started!')
            else:
                self.throw_error('Trigger mode ON!')

    def coder_power_btn_cmd(self):
        if self.udp_send('L'.encode()):
            if not self.coder_power:
                self.udp_send('CP'.encode())
                self.coder_power = True
                self.coder_power_btn['text'] = 'POWER OFF'
                self.udp_send('L'.encode())
            else:
                self.udp_send('Cp'.encode())
                self.coder_power = False
                self.coder_start = False
                self.coder_trigger = False
                self.coder_start_btn['state'] = ACTIVE
                self.coder_power_btn['text'] = 'POWER ON'
                self.coder_trigger_btn['text'] = 'TRIGGER ON'
                self.udp_send('L'.encode())

    def coder_start_btn_cmd(self):
        if self.udp_send('L'.encode()):
            if not self.coder_start and self.coder_power:
                self.udp_send('CS'.encode())
                self.coder_start = True
                self.coder_start_btn['state'] = DISABLED
            self.udp_send('L'.encode())

    def coder_trigger_btn_cmd(self):
        if self.udp_send('L'.encode()):
            if not self.coder_trigger and self.coder_start:
                self.udp_send('CT'.encode())
                self.coder_trigger = True
                self.coder_trigger_btn['text'] = 'TRIGGER OFF'
            else:
                self.udp_send('Ct'.encode())
                self.coder_trigger = False
                self.coder_trigger_btn['text'] = 'TRIGGER ON'
            self.udp_send('L'.encode())

    def coder_status_callback(self):
        count = 0
        while count < 100:
            res = self.udp_receive(self.BUFFER_SIZE)
            if res is None:
                count += 1
            elif res[:2] == '63':  # char 'c'
                self.coder_power = bool(int(res[3]))
                self.coder_start = bool(int(res[5]))
                self.coder_trigger = bool(int(res[7]))

                if not self.coder_power:
                    self.coder_power_btn['text'] = 'POWER ON'
                else:
                    self.coder_power_btn['text'] = 'POWER OFF'

                if not self.coder_start:
                    self.coder_start_btn['state'] = ACTIVE
                else:
                    self.coder_start_btn['state'] = DISABLED

                if not self.coder_trigger:
                    self.coder_trigger_btn['text'] = 'TRIGGER ON'
                else:
                    self.coder_trigger_btn['text'] = 'TRIGGER OFF'
                break

    def pmod_c_command(self):
        self.udp_send('L'.encode())
        self.udp_send(f'P{int(self.pmod_var.get())}'.encode())
        delay_ms(100)
        self.udp_send('L'.encode())
        self.connect_ddc()
        delay_ms(10)
        self.connect_ddc()

    def graph_nav_x_btn_command(self, _):
        try:
            val = int(self.graph_nav_x_e.get())
        except ValueError:
            self.bell()
            val = self.graph_len_max
        if val > self.graph_len_max:
            self.bell()
            val = self.graph_len_max
        elif val < 5:
            self.bell()
            val = 5
        self.graph_len = val

    def graph_nav_y_btn_command(self, _):
        try:
            val = int(self.graph_nav_y_e.get())
        except ValueError:
            self.bell()
            val = 35000
        if val > 35000:
            self.bell()
            val = 35000
        elif val < 10:
            self.bell()
            val = 10
        self.graph_scale = val

    def graph_btn_command(self):
        self.is_fft = not self.is_fft
        if self.is_fft:
            self.graph_btn['text'] = 'RAW'
        else:
            self.graph_btn['text'] = 'FFT'

    # -------------------------------------------------------- HELPER FUNCTIONS

    def release_udp_buffer(self):
        while True:
            res = self.udp_receive(self.BUFFER_SIZE)
            if res is None:
                return

    def getNCO(self, value: int) -> int:
        return round(2**32 * ((value * 1000) / self.fclock))

    def setDDCFs(self):
        try:
            clk = int(self.ddcClock_e.get()) * 1_000_000
            if clk:
                self.fclock = clk
        except ValueError:
            self.throw_error('Enter valid DDC Fc value in MHz')
            raise ValueError

    @staticmethod
    def hex2int(hexval):
        bits = 16
        val = int(hexval, 16)
        if val & (1 << (bits-1)):
            val -= 1 << bits
        return val

    @staticmethod
    def throw_warning(msg):
        messagebox.showwarning('Warning', msg)

    @staticmethod
    def throw_error(msg):
        messagebox.showerror('Error', msg)


DDC()
