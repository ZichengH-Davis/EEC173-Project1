import dpkt
import datetime
from collections import Counter
import socket  

pcap_path = "ftp.pcap"
f = open(pcap_path, 'rb')
pcap = dpkt.pcap.Reader(f)

counts = Counter() 
dest_list = [] 

for timestamp, data in pcap:
    ts = datetime.datetime.fromtimestamp(timestamp, datetime.UTC)

    eth = dpkt.ethernet.Ethernet(data)

    # do not proceed if there is no network layer data
    if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
        continue

    ip = eth.data

    if isinstance(ip, dpkt.ip.IP):
        dst_ip_str = socket.inet_ntoa(ip.dst) 
        ts_str = ts.strftime("%H:%M:%S.%f")
        dest_list.append((ts_str, dst_ip_str))


    # If it's ICMP, (we need it for ping google)
    if isinstance(ip, dpkt.ip.IP) and ip.p == dpkt.ip.IP_PROTO_ICMP:
        counts['ICMP (ping)'] += 1

    # do not proceed if there is no transport layer data
    if not isinstance(ip.data, dpkt.tcp.TCP) and not isinstance(ip.data, dpkt.udp.UDP):
        continue

    tcp = ip.data  
    # do not proceed if there is no application layer data
    if not len(tcp.data) > 0:
        continue

    sport = getattr(tcp, 'sport', None)
    dport = getattr(tcp, 'dport', None)
    ports = {sport, dport}

    if 80 in ports:
        counts['HTTP'] += 1
    elif 443 in ports:
        counts['HTTPS'] += 1
    elif (20 in ports) or (21 in ports):
        counts['FTP'] += 1
    elif 25 in ports:
        counts['SMTP'] += 1
    elif 53 in ports:
        counts['DNS'] += 1
    elif 443 in ports:
        counts['QUIC'] += 1
    elif 67 in ports or 68 in ports:
        counts['DHCP'] += 1
    elif 123 in ports:
        counts['NTP'] += 1
    elif 5353 in ports:
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

