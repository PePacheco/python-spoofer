from dnslib import *
import socket

class DNSHandler:
    def __init__(self):
        self.records = {
            'www.example.com.': '1.2.3.4',
        }

    def handle(self, data, addr):
        request = DNSRecord.parse(data)
        reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

        qname = str(request.q.qname)
        if qname in self.records:
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(self.records[qname]), ttl=60))
        else:
            reply.header.rcode = RCODE.NXDOMAIN

        sock.sendto(reply.pack(), addr)

def start_dns_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 53))

    handler = DNSHandler()

    while True:
        data, addr = sock.recvfrom(512)
        handler.handle(data, addr)

if __name__ == "__main__":
    start_dns_server()
