import time
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

ip = input("Target addr >> ")
closed = 0
openp = []


def isTargetUp(ip):
    icmp = IP(dst=ip) / ICMP()
    resp = sr1(icmp, timeout=10)
    if resp == None:
        return False
    else:
        return True


conf.verb = 0
start_time = time.time()
port_min = int(input("Port min: "))
port_max = int(input("Port max: ")) + 1
ports = range(port_min, port_max)


if isTargetUp(ip):

    print ("Host %s is up, start scanning" % ip)

    for port in ports:

        srcPort = RandShort()
        synPacket = IP(dst=ip) / TCP(sport=srcPort, dport=port, flags='S')
        resp = sr1(synPacket, timeout=2)

        if resp:
            if resp.haslayer(TCP):
                if resp.getlayer(TCP).flags == 0x12:
                    send_rst = sr(IP(dst=ip) / TCP(sport=srcPort, dport=port, flags='AR'), timeout=1)
                    print("[+] Port %s is open" % port)
                elif resp.getlayer(TCP).flags == 0x14:
                    print("[-] Port %s is closed" % port)
        else:
            print("[-] Port %s is closed" % port)
    duration = time.time() - start_time
    print("%s Scan Completed in %fs" % (ip, duration))
