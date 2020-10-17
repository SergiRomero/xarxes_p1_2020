import socket
import select

IP = "192.168.1.48"     # Server ip
PORT = 1234             # Server port

#
#   Recives and returns a message from specified socket
#
def recive_message (client_socket):
    try:
        message = client_socket.recv(1024)
        return message.decode()
    except:
        return False

#
#   Register a new client. Stores socket to resend messages and client data
#
def save_new_client(socket, username, client_address):
    
    sockets_list.append(socket)
    clients[socket] = username # Save client data

    print("Accepted new conection from ", client_address," by ", clients[socket])

    socket.send(str.encode("SERVER : Wellcome " + username + " to the chat room!\nSERVER : " + ', '.join(str(username) for username in list(clients.values())) + " are online now!"))

    resend_to_all_clients(socket, "SERVER : " + username + " joined the room")

# 
#   Removes given client from registered sockets and client data
# 
def unsubscribe_client(client_socket):
    
    print("Close conection from " + clients[client_socket])
    resend_to_all_clients(client_socket, "SERVER : " + clients[client_socket] + " left the room ;(")
    sockets_list.remove(client_socket)
    del clients[client_socket]


#
#   Message view to be returned to clients
#
def out_message(client_socket, message):

    return clients[recived_socket] + " : " + message

#
#   Sends a given message to all clients except for a given (who send the message)
#
def resend_to_all_clients(sender_socket, message):

    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(str.encode(message))


#
#   Accepts socket and register new client
#
def handle_new_client(recived_socket):

    client_socket, client_address = server_socket.accept()
    message = recive_message(client_socket)

    if not message:
        return

    save_new_client(client_socket, message, client_address)


#
#   Reads recieved message and resends it to all clients
#
def handle_message(recived_socket):

    message = recive_message(recived_socket)

    if not message:
        # Empty socket means conection closed by client
        unsubscribe_client(recived_socket)
        return
    
    print("Recived message >> " + out_message(recived_socket, message))

    # Send recived message to other clients
    resend_to_all_clients(recived_socket, out_message(recived_socket, message))


#
#=================================================================
#
#                           MAIN
#
#=================================================================
#

#Init socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Listen on defined port
server_socket.bind((IP, PORT))
server_socket.listen()
print("Listening on ", (IP, PORT))

# Client data
sockets_list = [server_socket]
clients = {} #{socket: username}

while True:

    read_sockets, _, exception_sockets = select.select(sockets_list, [], [])
    
    for recived_socket in read_sockets:
    
        if recived_socket == server_socket:
            handle_new_client(recived_socket)

        else:
            handle_message(recived_socket)
    

    # If error ocurred close socket with client
    for s in exception_sockets:
        unsubscribe_client(recived_socket)

