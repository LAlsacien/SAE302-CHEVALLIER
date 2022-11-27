import socket

host = "127.0.0.1"
port = 10000
usnameserver = "Serveur"
data = ""

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((host, port))
socket_server.listen(1)

while True:
    conn, address = socket_server.accept()
    usname = conn.recv(1024).decode()
    conn.send(usnameserver.encode())
    while data!="exit" and data!="bye":
        data = conn.recv(2048).decode()
        print(f"\n{usname} > {data}")
        msg = input(f'\n{usnameserver} > ')
        conn.send(msg.encode())
    conn.close()
    rep = input("Continuer ? (y/n)")
    if rep == "n":
        break
socket_server.close()


