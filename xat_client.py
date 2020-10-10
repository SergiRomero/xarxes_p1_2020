import socket
import select



IP = "127.0.0.1"
PORT = 1234
username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False) # Dont block connection

client_socket.send(str.encode(username)) # Encode and send username to stablish connection

while True:
    new_message = input(username + ">> ")
    
    if new_message:
        client_socket.send(str.encode(new_message))
    
    try:
        message = client_socket.recv(1024)
        print(message.decode())
    
    except IOError as e:
        # Error when we read and nothing to read
        pass
