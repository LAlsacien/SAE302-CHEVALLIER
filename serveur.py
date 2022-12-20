import socket
import sys
import platform
import subprocess
import psutil

host = "0.0.0.0"
port = 10000
usnameserver = platform.system() + " " + platform.release()
print(usnameserver)
os = platform.system()
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
                    envoi = f"Commande spécifiée : CPU ---> {psutil.cpu_percent()}% utilisé."
                    conn.send(envoi.encode())
                elif data == "ip":
                    ip_address = "Non disponible"
                    try:
                        ip_address = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]
                    except:
                        pass
                    envoi = f"Commande spécifiée : IP ---> {ip_address}"
                    conn.send(envoi.encode())
                elif data == "nom":
                    envoi = f"Commande spécifiée : NOM ---> {platform.node()}"
                    conn.send(envoi.encode())
                elif data == "ram":
                    envoi = f"Commande spécifiée : RAM ---> {round(psutil.virtual_memory()[3]/1000000000, 2)}Go / {round(psutil.virtual_memory()[0]/1000000000, 2)}Go --> {round(psutil.virtual_memory()[4]/1000000000, 2)}Go libre."
                    conn.send(envoi.encode())
                else:
                    if data != "kill" and data!="reset" and data!="disconnect":
                        datad = data.split(':')
                        print(f"{datad[0]} & {datad[1]}")
                        if datad[0] == '*':
                            try:
                                if os == 'Windows':
                                    print("Hello Windows!")
                                    result = subprocess.run(["powershell", "-NonInteractive", "-Command", datad[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                    result2 = result.stdout.decode('cp1252')
                                else:
                                    result = subprocess.run(datad[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                    result2 = result.stdout.decode('cp1252')
                            except subprocess.CalledProcessError as err:
                                print(err)
                                result2 = "Échec de la commande. Veuillez vérifier la syntaxe ou vérifier s'il ne manque pas des arguments."
                                envoi = f"Commande spécifiée : {datad[1]} ---> {result2}"
                                conn.send(envoi.encode())
                            else:
                                if result2 == '':
                                    result2 = 'Commande effectuée.'
                                envoi = f"Commande spécifiée : {datad[1]} ---> {result2}"
                                conn.send(envoi.encode())
                        elif datad[0] == 'powershell':
                            if os != 'Windows':
                                result2 = 'Le système d\'exploitation ne prend pas en charge le terminal que vous souhaitez utiliser. Veuillez changer de terminal.'
                                envoi = f"Commande spécifiée : {datad[1]} ---> {result2}"
                                conn.send(envoi.encode())
                            else:
                                try:
                                    print("OK")
                                    result = subprocess.run(["powershell", "-NonInteractive", "-Command", datad[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                    result2 = result.stdout.decode('cp1252')
                                except subprocess.CalledProcessError as err:
                                    print(err)
                                    result2 = "Échec de la commande. Veuillez vérifier la syntaxe ou vérifier s'il ne manque pas des arguments."
                                    envoi = f"Commande spécifiée : {datad[1]} ---> {result2}"
                                    conn.send(envoi.encode())
                                else:
                                    if result2 == '':
                                        result2 = 'Commande effectuée.'
                                    envoi = f"Commande spécifiée : {datad[1]} ---> {result2}"
                                    conn.send(envoi.encode())
                        elif datad[0] == 'linux':
                            if os != 'Linux':
                                result2 = 'Le système d\'exploitation ne prend pas en charge le terminal que vous souhaitez utiliser. Veuillez changer de terminal.'
                                envoi = f"Commande spécifiée : {datad[1]} ---> {result2}"
                                conn.send(envoi.encode())
                            else:
                                try:
                                    result = subprocess.run(datad[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                    result2 = result.stdout.decode('cp1252')
                                except subprocess.CalledProcessError as err:
                                    print(err)
                                    result2 = "Échec de la commande. Veuillez vérifier la syntaxe ou vérifier s'il ne manque pas des arguments."
                                    envoi = f"Commande spécifiée : {datad[1]} ---> {result2}"
                                    conn.send(envoi.encode())
                                else:
                                    if result2 == '':
                                        result2 = 'Commande effectuée.'
                                    envoi = f"Commande spécifiée : {datad[1]} ---> {result2}"
                                    conn.send(envoi.encode())
                        elif datad[0] == 'dos':
                            if os != 'Darwin':
                                result2 = 'Le système d\'exploitation ne prend pas en charge le terminal que vous souhaitez utiliser. Veuillez changer de terminal.'
                                envoi = f"Commande spécifiée : {datad[1]} ---> {result2}"
                                conn.send(envoi.encode())
                            else:
                                try:
                                    result = subprocess.run(datad[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                    result2 = result.stdout.decode('cp1252')
                                except subprocess.CalledProcessError as err:
                                    print(err)
                                    result2 = "Échec de la commande. Veuillez vérifier la syntaxe ou vérifier s'il ne manque pas des arguments."
                                    envoi = f"Commande spécifiée : {datad[1]} ---> {result2}"
                                    conn.send(envoi.encode())
                                else:
                                    if result2 == '':
                                        result2 = 'Commande effectuée.'
                                    envoi = f"Commande spécifiée : {datad[1]} ---> {result2}"
                                    conn.send(envoi.encode())
                    else:
                        pass  
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