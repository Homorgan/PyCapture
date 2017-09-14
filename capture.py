import pyshark
from redis import Redis
import json

cap = pyshark.LiveCapture(interface='en0')

def redis_push(protocol, data):
    try:
        redis = Redis(host='localhost', db=0, socket_timeout=5)
        redis.rpush(protocol, data)
    except AttributeError as e:
        pass

def print_conversation_header(pkt):
    try:
        protocol =  pkt.transport_layer
        src_addr = pkt.ip.src
        src_port = pkt[pkt.transport_layer].srcport
        dst_addr = pkt.ip.dst
        dst_port = pkt[pkt.transport_layer].dstport
        if 'TCP' in pkt:
            flags = pkt.tcp.flags
            ack = pkt.tcp.flags_ack
            fin = pkt.tcp.flags_fin
            syn = pkt.tcp.flags_syn
            time = str(pkt.sniff_time)
            stamp = str(pkt.sniff_timestamp)
            data = json.dumps({'Prot': protocol, 'SRC': src_addr, 'SRC-Port': src_port, 'DST': dst_addr, 'DST-Port': dst_port, 'Flags': flags, 'Fin': fin, 'Ack': ack, 'Syn': syn, 'Stamp': stamp, 'Time': time})
        else:
            data = json.dumps({'Prot': protocol, 'SRC': src_addr, 'SRC-Port': src_port, 'DST': dst_addr, 'DST-Port': dst_port})
        # print '%s  %s:%s --> %s:%s' % (protocol, src_addr, src_port, dst_addr, dst_port)
        # data = json.dumps({'Prot': protocol, 'SRC': src_addr, 'SRC-Port': src_port, 'DST': dst_addr, 'DST-Port': dst_port})
        redis_push(protocol, data)
    except AttributeError as e:
        #ignore packets that aren't TCP/UDP or IPv4
        # print '%s %s --> %s' % (pkt.ip.proto, pkt.ip.src, pkt.ip.dst)
        # print(pkt.layers)
        pass

cap.apply_on_packets(print_conversation_header)

# python capture.py > /dev/null 2>&1 & disown
