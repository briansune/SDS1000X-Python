import socket
import sys
import time
from numpy import arange


# import pyvisa as visa

class SDS1000X:

    def __init__(self):
        self.sds_ip = ''
        self.sds_port = 5025
        self.sds_socket = socket.socket()
        self.volt_div = 0
        self.volt_ofs = 0
        self.time_ofs = 0
        self.time_div = 0
        self.smpl_rat = 0
        self.time_axis = []
        self.volt_axis = []
        self.plot_x = []
        self.plot_y = []

    def sds_connect(self):
        try:
            self.sds_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket.')
            return

        try:
            self.sds_socket.connect((self.sds_ip, self.sds_port))
        except socket.error:
            print('failed to connect to ip ' + self.sds_ip)
            return

        self.sds_setup('BUZZ ON')

    def sds_setup(self, cmd):
        try:
            self.sds_socket.sendall('{}\n'.format(cmd).encode())
            time.sleep(0.1)
        except socket.error:
            print('Send failed')
            sys.exit()

    def sds_query(self, cmd):
        try:
            self.sds_socket.sendall('{}\n'.format(cmd).encode())
            time.sleep(0.1)
        except socket.error:
            print('Send failed')
            sys.exit()
        while True:
            reply = self.sds_socket.recv(4096)
            if reply:
                return reply.strip().decode()

    def sds_channel_query(self, ch, cmd):
        try:
            self.sds_socket.sendall('C{}:{}\n'.format(ch, cmd).encode())
            time.sleep(0.1)
        except socket.error:
            print('Send failed')
            sys.exit()
        while True:
            reply = self.sds_socket.recv(4096)
            if reply:
                return reply.strip().decode()

    def sds_channel_capture(self, ch):
        try:
            self.sds_socket.sendall('C{}:{} {}\n'.format(ch, 'WF?', 'DAT2').encode())
            time.sleep(0.3)
        except socket.error:
            print('Send failed')
            sys.exit()
        reply = self.sds_socket.recv(22)
        arlen = 0
        if reply:
            arlen = int(reply.decode()[14:])
            # print(reply)
            # print(arlen)
        if not arlen:
            return False
        reply = b''
        cnt = 0
        while cnt < arlen:
            raw = self.sds_socket.recv(4096)
            reply += raw
            cnt += len(raw)

        byt_raw = [int('{:02x}'.format(x), 16) for x in reply[:-2]]
        byt_raw = [x if x < 128 else x - 255 for x in byt_raw]
        self.plot_y = [v * (self.volt_div / 25) for v in byt_raw]
        time_cal_s = self.time_ofs - (self.time_div * 14 / 2)
        time_smpl = 1 / self.smpl_rat
        time_cal_e = time_cal_s + self.time_div * 14
        self.plot_x = [v for v in arange(time_cal_s, time_cal_e, time_smpl)]
        self.volt_axis = [-4.0 * self.volt_div, 4.0 * self.volt_div]
        self.time_axis = [time_cal_s, time_cal_e]

        return True

    def sds_close(self):
        self.sds_setup('BUZZ OFF')
        self.sds_socket.close()

    def sds_get_stage(self):
        a_testcase = [
            self.sds_query('BUZZ?'),
            self.sds_query('ALST?'),
            self.sds_query('HPOS?'),
            self.sds_query('TDIV?'),
            self.sds_query('TRMD?'),
            self.sds_query('TRSE?'),
            self.sds_query('TRDL?'),
            self.sds_query('ACQW?'),
            self.sds_query('SARA?'),
            self.sds_channel_query(1, 'OFST?'),
            self.sds_channel_query(1, 'TRA?'),
            self.sds_channel_query(1, 'TRCP?'),
            self.sds_channel_query(1, 'TRSL?'),
            self.sds_channel_query(1, 'TRLV?'),
            self.sds_channel_query(1, 'TRLV2?'),
            self.sds_channel_query(1, 'VDIV?'),
            self.sds_channel_query(1, 'CPL?')
        ]
        for c in a_testcase:
            print(c)

    def sds_get_scop_cfg(self, ch):

        def scrop(s):
            return s.split(' ')[1]

        self.volt_div = float(scrop(self.sds_channel_query(ch, 'VDIV?'))[:-1])
        self.volt_ofs = float(scrop(self.sds_channel_query(ch, 'OFST?')[:-1]))
        self.time_ofs = float(scrop(self.sds_query('TRDL?')[:-1]))
        self.time_div = float(scrop(self.sds_query('TDIV?')[:-1]))
        self.smpl_rat = float(scrop(self.sds_query('SARA?')[:-4]))
