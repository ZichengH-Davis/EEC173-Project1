import dpkt

f = open("PCAP1_1.pcap", "rb")
pcap = dpkt.pcap.Reader(f)

i = 0
for timestamp, buf in pcap:
    i += 1
    if i != 112:
        continue  

    eth = dpkt.ethernet.Ethernet(buf)
    ip = eth.data
    tcp = ip.data
    payload = tcp.data

    text = payload.decode('utf-8', errors='replace')

    print(text)
    break  

f.close()
