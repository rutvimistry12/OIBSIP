import socket
import threading
from cryptography.fernet import Fernet

HOST = '127.0.0.1'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

key = Fernet.generate_key()
cipher = Fernet(key)

print("Server started...")

def broadcast(message):
    encrypted = cipher.encrypt(message)
    for client in clients:
        client.send(encrypted)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            decrypted = cipher.decrypt(message)
            broadcast(decrypted)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            usernames.remove(username)
            broadcast(f"{username} left the chat.".encode())
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")
        client.send(key)
        username = cipher.decrypt(client.recv(1024)).decode()
        usernames.append(username)
        clients.append(client)
        broadcast(f"{username} joined the chat.".encode())
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
