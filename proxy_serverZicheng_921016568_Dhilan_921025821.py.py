import socket
import json

HOST = '127.0.0.1'
PORT = 5500

# create a new TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # bind this socket to OS
    server_socket.bind((HOST, PORT))

    # set listening mode on for this socket
    server_socket.listen()
    
    # run indefinitely
    while True:
        # wait for and accept a new connection
        # client_socket -> socket to communicate with client
        # client_addr -> client's IP address, client_port -> client's port number
        client_socket, (client_addr, client_port) = server_socket.accept()
        

        # receive data just once from client
        data = client_socket.recv(1024)
        string_data = json.loads(data)
        
        
        print(string_data["server_ip"])
        if string_data["server_ip"] != "127.0.0.1":
            print("error")
            client_socket.sendall(b"error")
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as actual_server_socket:
                actual_server_socket.connect((string_data["server_ip"], string_data["server_port"]))
       
                actual_server_socket.sendall(string_data["message"].encode('utf-8'))
                response = actual_server_socket.recv(1024)

                actual_server_socket.close()
            
            client_socket.sendall(response)








        

