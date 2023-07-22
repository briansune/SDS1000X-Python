import socket
import sys
import time

# bit 13    Trigger Ready
# bit 12    Pass/Fail
# bit 11    Trace D
# bit 10    Trace C
# bit  9    Trace B
# bit  8    Trace A

spd_ip = '192.168.1.240'
spd_port = 5025
spd_mode = False
spd_output = False
spd_wires = False
spd_timer = False
spd_disp = False
spd_lock = False
spd_mea_volt = 0.0
spd_mea_curr = 0.0

spd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    spd_socket.connect((spd_ip, spd_port))
except socket.error:
    print('fail')

spd_socket.sendall(b'BUZZ ON\n')
spd_socket.sendall(b'BUZZ?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'ALST?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'CMR?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'DDR?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'HPOS?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'C1:OFST?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'TDIV?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'C2:TRA ON\n')
spd_socket.sendall(b'C2:TRA OFF\n')

spd_socket.sendall(b'C1:TRA?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'C1:TRCP?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)


spd_socket.sendall(b'C1:TRLV?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'C1:TRLV2?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'TRMD?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'TRSE EDGE,SR,C1,HT,OFF\n')

spd_socket.sendall(b'TRSE?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'C1:TRSL?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'C1:VDIV?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'ACQW?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'C1:CPL?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'INR?\n')

reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode().split(' ')
    print(b)

spd_socket.sendall(b'*ESR?\n')
reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode()
    print(b)

spd_socket.sendall(b'ASET\n')

spd_socket.sendall(b'INR?\n')

reply = spd_socket.recv(4096)
if reply:
    b = reply.strip().decode().split(' ')
    print(b)

spd_socket.close()
