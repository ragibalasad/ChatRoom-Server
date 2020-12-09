import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT) 
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
CONN = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    CONN.append(conn)

    connected = True
    while connected:
        msg_lenght = conn.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            msg = conn.recv(msg_lenght).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[{addr}] {DISCONNECT_MESSAGE}")
            else:
                print(f"[{addr}] {msg}")
                with open("messages.txt", "a") as f:
                    f.write(msg)

                for i in CONN:
                    try:
                        i.send(bytes(msg, FORMAT))
                    except:
                        pass
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}...")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()