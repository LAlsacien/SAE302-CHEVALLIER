import socket
import sys
import platform

host = "0.0.0.0"
port = 10000
usnameserver = platform.system() + " " + platform.release()
data = ""

while data != "kill":
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))
    socket_server.listen(1)
    print('Listen ok')
    while data != "kill" and data != "reset":
        try:
            print('En attente du client')
            conn, address = socket_server.accept()
            print(f'client connecté à partir de {address}')
            usname = conn.recv(1024).decode()
            conn.send(usnameserver.encode())
        except socket.error:
            data = "reset"
        else:
            while data!="kill" and data!="reset" and data!="disconnect":
                data = conn.recv(2048).decode()
                data = data.lower()
                print(data)
                if data == "os":
                    envoi = f"Commande spécifiée : OS ---> {platform.system()} {platform.release()}"
                    conn.send(envoi.encode())
                elif data == "cpu":
                    envoi = f"Commande spécifiée : CPU --->"
                    conn.send(envoi.encode())
                elif data == "ip":
                    envoi = f"Commande spécifiée : IP --->"
                    conn.send(envoi.encode())
                elif data == "nom":
                    envoi = f"Commande spécifiée : NOM --->"
                    conn.send(envoi.encode())
                elif data == "ram":
                    envoi = f"Commande spécifiée : RAM --->"
                    conn.send(envoi.encode())
                else:
                    envoi = f"Commande spécifiée introuvable."
                    conn.send(envoi.encode())


            if data == "disconnect":
                data = ""
                print(f"Déconnecté avec succès.")
            conn.close()
    if data == "reset":
        data = ""
        print(f"Réinitialié avec succès.")

    print('Socket serveur close')
    socket_server.close()
sys.exit(0)