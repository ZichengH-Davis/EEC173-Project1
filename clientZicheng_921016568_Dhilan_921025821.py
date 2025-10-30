import socket
import json

# specify server host and port to connect to
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5500

data = {
    "server_ip": "127.0.0.1", # The server's IP (destination)
    "server_port": 7000, # The server's port (destination)
    "message": "ping" # The actual message
}

json_string = json.dumps(data)
encoded_data = json_string.encode('utf-8')

# create a new TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))

    s.sendall(encoded_data)

    data = s.recv(1024)
    print(f"Received {data.decode()!r} from {SERVER_HOST}:{SERVER_PORT}")




