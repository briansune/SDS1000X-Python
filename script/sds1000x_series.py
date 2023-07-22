import socket
import sys
import time


# import pyvisa as visa

class SDS1000X:

    def __init__(self):
        self.sds_ip = ''
        self.sds_port = 5025
        self.sds_socket = socket.socket()

    def sdsConnect(self):
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

        self.sdsSetup('BUZZ ON')

    def sdsSetup(self, cmd):
        try:
            self.sds_socket.sendall('{}\n'.format(cmd).encode())
            time.sleep(0.1)
        except socket.error:
            print('Send failed')
            sys.exit()

    def sdsQuery(self, cmd):
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

    def sdsChannelQuery(self, ch, cmd):
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

    def sdsClose(self):
        self.sdsSetup('BUZZ OFF')
        self.sds_socket.close()

    def sdsGetStage(self):
        a_testcase = [
            self.sdsQuery('BUZZ?'),
            self.sdsQuery('ALST?'),
            self.sdsQuery('HPOS?'),
            self.sdsQuery('TDIV?'),
            self.sdsQuery('TRMD?'),
            self.sdsQuery('TRSE?'),
            self.sdsQuery('ACQW?'),
            self.sdsChannelQuery(1, 'OFST?'),
            self.sdsChannelQuery(1, 'TRA?'),
            self.sdsChannelQuery(1, 'TRCP?'),
            self.sdsChannelQuery(1, 'TRSL?'),
            self.sdsChannelQuery(1, 'TRLV?'),
            self.sdsChannelQuery(1, 'TRLV2?'),
            self.sdsChannelQuery(1, 'VDIV?'),
            self.sdsChannelQuery(1, 'CPL?')
        ]
        for c in a_testcase:
            print(c)
