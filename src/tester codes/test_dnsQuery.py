#from dust i have come, dust i will be

from DNS_QueryBuilder import *

def send_udp(msg ,server_ip, port):
        # no blank or newline
        msg = msg.replace(" ", "").replace("\n", "")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            sock.sendto(binascii.unhexlify(msg), (server_ip, port))
            print(binascii.unhexlify(msg))

            data, address = sock.recvfrom(4096)
        finally:
            sock.close()

        return binascii.hexlify(data).decode("utf-8")
    
    
q = dns_query()
q.setShowError(True)
q.setShowReport(True)
q.setDomainName("codeforces.com")

ques = q.getDNSQuery()
print(ques)
res = send_udp(ques,"192.168.0.104", 53)
print(q.getIP(res))  
