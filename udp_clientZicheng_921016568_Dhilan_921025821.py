import socket
import time

# specify server host and port to connect to
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5500
total_bytes_to_send = 100 * 1024 * 1024

# open a new datagram socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    #each chunk is 1024 because that is how much server said in recvfrom(1024)
    chunk = b'a' * 1024 
    
    bytes_sent = 0


    while bytes_sent < total_bytes_to_send:
        client_socket.sendto(chunk, (SERVER_HOST, SERVER_PORT))
        bytes_sent += len(chunk)

    # tell server if done
    client_socket.sendto(b"DONE", (SERVER_HOST, SERVER_PORT))

    #recieve throughput result from server and print
    data, addr = client_socket.recvfrom(1024)
    print("throughput:", data)
