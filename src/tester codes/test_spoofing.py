# from dust i have come, dust i will be

import socket
from DNS_QueryBuilder import *
from scapy.all import *

src_ip = '192.168.0.106'
dest_ip = '8.8.8.8'

src_port = 107
dest_port = 53

# --------------------------------
# dns query
q = dns_query()
q.setShowError(True)
q.setShowReport(True)
q.setDomainName("codeforces.com")

payload = q.getDNSQuery()
payload = binascii.unhexlify(payload)
# --------------------------------


spoofed_packet = IP(src=src_ip, dst=dest_ip) / UDP(sport=src_port, dport=dest_port) / payload
send(spoofed_packet)

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data, address = sock2.recvfrom(4096)
print(q.getIP(binascii.hexlify(data).decode("utf-8")), address)