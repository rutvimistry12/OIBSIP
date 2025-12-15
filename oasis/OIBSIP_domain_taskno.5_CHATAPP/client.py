import socket
import threading
import tkinter as tk
from cryptography.fernet import Fernet

HOST = '127.0.0.1'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

key = client.recv(1024)
cipher = Fernet(key)

def receive():
    while True:
        try:
            message = cipher.decrypt(client.recv(1024)).decode()
            chat_box.config(state='normal')
            chat_box.insert(tk.END, message + "\n")
            chat_box.config(state='disabled')
        except:
            break

def send():
    message = f"{username}: {msg_entry.get()}"
    client.send(cipher.encrypt(message.encode()))
    msg_entry.delete(0, tk.END)

def login():
    global username
    username = user_entry.get()
    client.send(cipher.encrypt(username.encode()))
    login_frame.destroy()
    chat_frame.pack()
    threading.Thread(target=receive).start()

root = tk.Tk()
root.title("Chat Application")

login_frame = tk.Frame(root)
tk.Label(login_frame, text="Username").pack()
user_entry = tk.Entry(login_frame)
user_entry.pack()
tk.Button(login_frame, text="Login", command=login).pack()
login_frame.pack()

chat_frame = tk.Frame(root)
chat_box = tk.Text(chat_frame, state='disabled')
chat_box.pack()
msg_entry = tk.Entry(chat_frame)
msg_entry.pack(fill=tk.X)
tk.Button(chat_frame, text="Send", command=send).pack()

root.mainloop()
