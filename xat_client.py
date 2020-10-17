import socket
import threading


IP = "192.168.1.48"     # Server ip 
PORT = 1234             # Server Port

"""
    Waits for user input and sends the socket to server
"""
def write_new_message(client_socket, username):
    while True:
        new_message = input()
        
        if new_message:
            client_socket.send(str.encode(new_message))


"""
    Checks if recived socket and prints it if recived
"""
def printRecivedMessages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            print(message.decode())
        
        except IOError:
            # There is no message to read
            pass



# Identifies user on chat room
username = input("Username: ")

#Init socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False) # Dont block connection

client_socket.send(str.encode(username)) # Encode and send username to stablish connection

# Create two threads to  paralelize send and recive message
write_thread = threading.Thread(target=write_new_message, args=(client_socket, username))
read_thread = threading.Thread(target=printRecivedMessages, args=(client_socket,))

write_thread.start()
read_thread.start()