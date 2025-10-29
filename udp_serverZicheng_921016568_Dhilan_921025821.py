import socket
import time

# specify host and port to receive messages on
HOST = '127.0.0.1'
PORT = 5500

# create a new datagram socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    # bind this socket to OS
    server_socket.bind((HOST, PORT))

    total_bytes = 0
    start_time = None
    end_time = None

    # receive messages indefinitely
    while True:
        data, addr = server_socket.recvfrom(1024)
        # if first packet, start timer
        if start_time is None and data != b"DONE":
            start_time = time.time()
        # check for done signal
        if data == b"DONE":
            end_time = time.time()
            break

        total_bytes += len(data)

    total_time = end_time - start_time 
    bytes_per_sec = total_bytes / total_time
    kb_per_sec = bytes_per_sec / 1024 
    result_msg = f"{kb_per_sec} kB/s"

    server_socket.sendto(result_msg.encode('utf-8'), addr)

    