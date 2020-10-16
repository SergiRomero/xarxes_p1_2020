import socket
import select

IP = "192.168.1.48"
PORT = 1234


#Init socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Listen on defined port
server_socket.bind((IP, PORT))
server_socket.listen()
print("Listening on ", (IP, PORT))

# Client data
sockets_list = [server_socket]
clients = {} #{socket: user_data}

def recive_message (client_socket):
    try:
        message = client_socket.recv(1024) #Harcoded lenght

        # TODO: If no data do something

        return message
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], [])
    
    for s in read_sockets:

        if s == server_socket:
            client_socket, client_address = server_socket.accept() # Socket de subscripció. Utilitza el socket que hem obert per establir la comunicació
            message = recive_message(client_socket)

            if not message:
                continue

            sockets_list.append(client_socket) # Register new client
            clients[client_socket] = message.decode()

            print("Accepted new conection from ", message.decode())

        else:
            message = recive_message(s)

            if not message:
                print("Close conection from someone") # TODO: Provide decent feedback
                sockets_list.remove(s)
                del clients[s]
                continue
            
            print("Recived message from " + clients[s] + ": " + message.decode())

            for client_socket in clients:
                if client_socket != s:
                    out_text = clients[s] + ": " + message.decode()
                    client_socket.send(str.encode(out_text))

    for s in exception_sockets:
        sockets_list.remove(s)
        del clients[s]
















