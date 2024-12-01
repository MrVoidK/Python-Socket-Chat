import socket
import threading

HEADER = 64
PORT = 1234 
SERVER = socket.gethostbyname(socket.gethostname()) #use the local ip adress of device
ADDR = (SERVER, PORT) #address for bind
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT" #to disconnect

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#AF_INET = IPv4 protocol / SOCK_STREAM = TCP protocol
server.bind(ADDR) #it's assign socket to IP and PORT

def handle_client(conn, addr):
    print(f"NEW CONNECTION {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg Received".encode(FORMAT))
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNETIONS] {threading.active_count() - 1}")

print(">[STARTING] server is starting...")
start()