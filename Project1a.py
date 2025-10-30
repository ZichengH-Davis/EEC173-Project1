import dpkt
import datetime
from collections import Counter
import socket  

pcap_path = "google.pcap"
f = open(pcap_path, 'rb')
pcap = dpkt.pcap.Reader(f)

counts = Counter() 
dest_list = [] 
seen_ips = set() #for recording which ip have been seen

for timestamp, data in pcap:
    ts = datetime.datetime.fromtimestamp(timestamp, datetime.UTC)

    eth = dpkt.ethernet.Ethernet(data)

    # do not proceed if there is no network layer data
    if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
        continue

    ip = eth.data

    if isinstance(ip, dpkt.ip.IP):
        ip_addr = socket.inet_ntoa(ip.dst) 

    if ip_addr not in seen_ips:
        seen_ips.add(ip_addr)
        tstamp = ts.strftime("%H:%M:%S.%f")
        dest_list.append((tstamp, ip_addr))


    # If it's ICMP, (we need it for ping google)
    if isinstance(ip, dpkt.ip.IP) and ip.p == dpkt.ip.IP_PROTO_ICMP:
        counts['ICMP (ping)'] += 1

    # do not proceed if there is no transport layer data
    if not isinstance(ip.data, dpkt.tcp.TCP) and not isinstance(ip.data, dpkt.udp.UDP):
        continue

    transport_layer = ip.data  
    # do not proceed if there is no transport_layerlication layer data
    if not len(transport_layer.data) > 0:
        continue

    is_tcp = isinstance(transport_layer, dpkt.tcp.TCP)
    is_udp = isinstance(transport_layer, dpkt.udp.UDP)

    if is_tcp and (transport_layer.dport == 80 or transport_layer.sport == 80):
        counts["HTTP"] += 1
    elif is_tcp and (transport_layer.dport == 443 or transport_layer.sport == 443):
        counts['HTTPS'] += 1
    elif is_udp and (transport_layer.dport == 443 or transport_layer.sport == 443):
        counts['QUIC'] += 1
    elif is_tcp and (transport_layer.dport == 20 or transport_layer.sport == 20 or transport_layer.dport == 21 or transport_layer.sport == 21):
        counts['FTP'] += 1
    elif is_tcp and (transport_layer.dport == 25 or transport_layer.sport == 25):
        counts['SMTP'] += 1
    elif transport_layer.dport == 53 or transport_layer.sport == 53:
        counts['DNS'] += 1
    elif is_udp and (transport_layer.dport == 5353 or transport_layer.sport == 5353):
        counts['mDNS'] += 1
    else:
        counts['Other App'] += 1
        



print(f"{pcap_path}:\n")
total = sum(counts.values())
print("Total:", total)
for name, c in sorted(counts.items()):
    print(f"{name}: {c}")

print("\nip:")
for tstamp, ip_addr in dest_list:
    print(f"{tstamp}  ->  {ip_addr}")

