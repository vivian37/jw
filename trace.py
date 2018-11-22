
__author__ = 'Suraj Singh Bisht, HHQ. ZHANG'
__credit__ = '["Suraj Singh Bisht",]'
__contact__ = 'contact@jinlab.cn'
__copyright__ = 'Copyright 2018 Dept. CSE SUSTech'
__license__ = 'Apache 2.0'
__Update__ = '2018-01-11 12:33:09.399381'
__version__ = '0.1'
__maintainer__ = 'HHQ. ZHANG'
__status__ = 'Production'

import random
import select
# import module
import socket
import struct
import time

from raw_python \
    import IPPacket, ICMPPacket, parse_icmp_header, parse_eth_header, parse_ip_header


def calc_rtt(time_sent):
    return time.time() - time_sent


def catch_trace_reply(s, ID, time_sent, timeout=10):
    # create while loop
    while True:
        starting_time = time.time()  # Record Starting Time

        # to handle timeout function of socket
        process = select.select([s], [], [], timeout)

        # check if timeout
        if not process[0]:
            return calc_rtt(time_sent), None, None

        # receive packet
        rec_packet, addr = s.recvfrom(2048)

        # extract icmp packet from received packet
        icmp = parse_icmp_header(rec_packet[20:28])

        # check identification
        if icmp['id'] == ID:
            return calc_rtt(time_sent), parse_ip_header(rec_packet[:20]), icmp


def single_trace_request(s, addr=None):
    # Random Packet Id
    pkt_id = random.randrange(10000, 65000)
    data = b'0000000000000000000000000000000000000000000000000000000000000000'
    seq = 1
    # Create ICMP Packet
    print(addr)
    print(pkt_id,socket.gethostbyname(addr),"**")
    packet1_1 = IPPacket(dst = socket.gethostbyname(addr),idf = 27891,ttl = 1,tol = 92).raw
    print("**", parse_ip_header(b'\x45\x00\x00\x5c\x6c\xf3\x00\x00\x01\x01\x13\x76\x0a\x15\x6f\x26\x0e\xd7\xb1\x26'))
    print("***",parse_ip_header(packet1_1))
    # packet2 = IPPacket(dst = socket.gethostbyname(addr),ttl = 2).raw
    # Send ICMP Packet
    for i in range(0,3):
        seq = seq + 256
        packet1_2 = ICMPPacket(_type=8, data=data, _seq=seq).raw
        packet1 = packet1_1 +packet1_2
        while packet1:
            sent = s.sendto(packet1, (socket.gethostbyname(addr), 12000))
            packet1 = packet1[sent:]
    print("end1")
    # while packet2:
    #     sent = s.sendto(packet2, (addr, 1))
    #     packet2 = packet2[sent:]

    return pkt_id


def main():
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    # take Input
    addr = input("[+] Enter Domain Name : ") or "www.sustc.edu.cn"
    print('TRACE {0} ({1}) the most jump is 30.'.format(addr, socket.gethostbyname(addr)))
    # Request sent

    ID = single_trace_request(s, addr = addr)

    # Catch Reply
    rtt, reply, icmp_reply = catch_trace_reply(s, ID, time.time())
    print("end")
    if reply:
        reply['length'] = reply['Total Length'] - 20  # sub header
        print('{0[length]} bytes reply from {0[Source Address]} ({0[Source Address]}): '
              'icmp_seq={1[seq]} ttl={0[TTL]} time={2:.2f} ms'
              .format(reply, icmp_reply, rtt*1000))

    # close socket
    s.close()
    return


if __name__ == '__main__':
    main()