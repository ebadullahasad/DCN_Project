import socket
import threading

EBAD_HOST = '127.0.0.1'
EBAD_PORT = 12345

ebad_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ebad_server.bind((EBAD_HOST, EBAD_PORT))
ebad_server.listen()

ebad_clients = []
ebad_nicknames = []

def ebad_broadcast(message):
    for ebad_client in ebad_clients:
        ebad_client.send(message)

def ebad_handle(ebad_client):
    while True:
        try:
            message = ebad_client.recv(1024)
            ebad_broadcast(message)
        except:
            index = ebad_clients.index(ebad_client)
            ebad_clients.remove(ebad_client)
            ebad_client.close()
            nickname = ebad_nicknames[index]
            ebad_nicknames.remove(nickname)
            break

def ebad_receive():
    while True:
        ebad_client, ebad_address = ebad_server.accept()
        print(f"Connected with {str(ebad_address)}")

        ebad_client.send("NICK".encode('utf-8'))
        nickname = ebad_client.recv(1024).decode('utf-8')
        ebad_nicknames.append(nickname)
        ebad_clients.append(ebad_client)

        print(f"Nickname of the client is {nickname}")
        ebad_broadcast(f"{nickname} joined the chat!\n".encode('utf-8'))
        ebad_client.send("Connected to the server!\n".encode('utf-8'))

        thread = threading.Thread(target=ebad_handle, args=(ebad_client,))
        thread.start()

print("Server running...")
ebad_receive()