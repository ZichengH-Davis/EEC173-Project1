import dpkt

f = open("PCAP1_1.pcap", "rb")
pcap = dpkt.pcap.Reader(f)

i = 0
for timestamp, data in pcap:
    i += 1
    if i != 112:
        continue  

    eth = dpkt.ethernet.Ethernet(data)
    ip = eth.data
    tcp = ip.data
    payload = tcp.data

    text = payload.decode()

    print(text)
    break  

f.close()

