import sys
from xml.dom.minidom import Attr
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import socket
import ipaddress

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  
        self.Toolbar()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        self.inf = QLabel("Commandes simples")
        self.buttos = QPushButton("OS")
        self.buttos.clicked.connect(self.oss)
        self.buttram = QPushButton("RAM")
        self.buttram.clicked.connect(self.rams)
        self.buttcpu = QPushButton("CPU")
        self.buttcpu.clicked.connect(self.cpus)
        self.buttip = QPushButton("IP")
        self.buttip.clicked.connect(self.ips)
        self.buttname = QPushButton("Nom")
        self.buttname.clicked.connect(self.noms)
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        #self.scrollBar=QScrollBar(self.chat)
        self.buttchos = QComboBox()
        self.buttchos.addItem('')
        self.buttchos.addItem('Powershell:')
        self.buttchos.addItem('Linux:')
        self.buttchos.addItem('DOS:')
        self.commands = QLineEdit()
        self.commands.setMaximumHeight(25)
        self.envoyer = QPushButton("Envoyer")
        self.envoyer.clicked.connect(self.envoi)
        self.conn = QLabel("IP du Serveur :")
        self.ip = QLineEdit()
        self.iport = QLineEdit()
        self.conn2 = QPushButton("Se connecter")
        self.conn2.clicked.connect(self.connect)
        self.ip.setMaximumHeight(25)
        self.iport.setMaximumHeight(25)
        self.saveip = QComboBox()
        self.saveip.addItem('')
        self.conn3 = QPushButton("Se connecter")
        self.conn3.clicked.connect(self.connect2)
        self.conn4 = QLabel("Historique :")
        grid.addWidget(self.inf, 0, 0)
        grid.addWidget(self.buttos, 1,0)
        grid.addWidget(self.buttram, 1, 1)
        grid.addWidget(self.buttcpu, 1, 2)
        grid.addWidget(self.buttip, 1, 3)
        grid.addWidget(self.buttname, 1, 4)
        grid.addWidget(self.chat, 2, 0, 3, 5)
        grid.addWidget(self.buttchos, 5, 0)
        grid.addWidget(self.commands, 5, 1, 1, 3)
        grid.addWidget(self.envoyer, 5, 4)
        grid.addWidget(self.conn, 6, 0)
        grid.addWidget(self.ip, 6, 1, 1, 2)
        grid.addWidget(self.iport, 6, 3)
        grid.addWidget(self.conn2, 6, 4)
        # grid.addWidget(self.saveip, 7, 1, 1, 3)
        # grid.addWidget(self.conn3, 7, 4)
        # grid.addWidget(self.conn4, 7, 0)
        widget.setLayout(grid)
        self.setWindowTitle("Gestionnaire de Serveurs")
        self.socket_client = None
        self.port = None
        self.host = None

    def Toolbar(self):
        quitter = QAction('&Quitter', self)
        disconnect = QAction('&Déconnecter', self)
        kill = QAction('&Tuer', self)
        reset = QAction('&Réinitialiser', self)
        quitter.setShortcut('Ctrl+Q')
        disconnect.setShortcut('Ctrl+D')
        kill.setShortcut('Ctrl+K')
        reset.setShortcut('Ctrl+R')
        quitter.setStatusTip('Quitter l\'application.')
        disconnect.setStatusTip('Se déconnecter du serveur.')
        kill.setStatusTip('Arrêter le serveur depuis l\'interface client.')
        reset.setStatusTip('Réinitialiser la connexion entre le client et le serveur.')
        quitter.triggered.connect(self.quitt)
        disconnect.triggered.connect(self.deconnection)
        reset.triggered.connect(self.reset)
        kill.triggered.connect(self.kill)
        self.statusBar()
        menubar = self.menuBar()
        Menu = menubar.addMenu('&Menu')
        Menu.addAction(quitter)
        Menu.addAction(disconnect)
        Menu.addAction(kill)
        Menu.addAction(reset)

    def quitt(self):
        try:
            bye = "disconnect"
            self.socket_client.send(bye.encode())
        except (socket.error, AttributeError):
            pass
        QApplication.exit(0)
        
    # Appeler lorsque le bouton se connecter est appelé
    def connect(self):
        try:
            try:
                if self.host != None:
                    pass
                else:
                    self.chat.append(f"Je me déconnecte de {self.host}:{self.port} <-- {self.serverpseudo}")
                bye = "disconnect"
                self.socket_client.send(bye.encode())
            except (TypeError, AttributeError, OSError):
                pass
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.ip.text() != "localhost":
                self.host = ipaddress.ip_address(self.ip.text())
            self.port = int(self.iport.text())
            if self.port > 65535 or self.port <= 0:
                self.port = None
        except ValueError:
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'avez pas entrée une IP ou un port correcte.')
            msg.setWindowTitle("Erreur !")
            msg.exec()
        else:
            try:
                self.host = str(self.ip.text())
                self.ip.setText("")
                self.iport.setText("")
                self.chat.append(f"Je me connecte sur le serveur {self.host} on {self.port}")
                self.socket_client.connect((self.host, self.port))
                print("Connecté!")
            except TypeError:
                msg = QMessageBox()
                msg.setText("Erreur !")
                msg.setInformativeText('Vous n\'avez pas entrée une IP ou un port correcte.')
                msg.setWindowTitle("Erreur !")
                self.chat.append("Une erreur est survenue. Veuillez vous référer à la fenêtre qui s'est affichée.")
                self.chat.append("____________________________________________\n")
                msg.exec()
            except socket.error as err:
                print(err)
                msg = QMessageBox()
                msg.setText("Erreur !")
                msg.setInformativeText(f'Connexion impossible ou refusée.')
                self.chat.append("Une erreur est survenue. Veuillez vous référer à la fenêtre qui s'est affichée.")
                self.chat.append("____________________________________________\n")
                msg.setWindowTitle("Erreur !")
                msg.exec()
            else:
                self.pseudo = "Client"
                self.socket_client.send(self.pseudo.encode())
                self.serverpseudo = self.socket_client.recv(1024).decode()
                self.chat.append(f"Connecté sur {self.host}:{self.port} <-- {self.serverpseudo} !")
                self.chat.append("____________________________________________\n")
            
                # entree = f"{self.host} {self.port} <-- {self.serverpseudo}"
                # test = 0
                
                # for i in range(0, len(self.saveip)):
                #     if self.saveip[i] == entree:
                #         test += 1
                #     else:
                #         pass
                
                # if test >= 0:
                #     pass
                # else:
                #     self.saveip.addItem(entree)
                #     test = 0

    def connect2(self):
            try:
                bye = "disconnect"
                self.socket_client.send(bye.encode())
            except (TypeError, AttributeError, OSError):
                pass
            
            try:
                self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.ipsplit = self.saveip.currentText()
                self.ipsplit = self.ipsplit.split(" ", 2)
                print(self.ipsplit)
                self.host = str(self.ipsplit[0])
                self.port = int(self.ipsplit[1])
                print(self.host)
                print(self.port)
            except IndexError:
                msg = QMessageBox()
                msg.setText("Erreur !")
                msg.setInformativeText('Aucun serveur n\'est enregistré.')
                msg.setWindowTitle("Erreur !")
                msg.exec()
            else:
                try:
                    self.chat.append(f"Je me connecte sur le serveur {self.host} on {self.port}")
                    self.socket_client.connect((self.host, self.port))
                    print("Connecté!")
                except socket.error as err:
                    print(err)
                    msg = QMessageBox()
                    msg.setText("Erreur !")
                    msg.setInformativeText('Connexion impossible ou refusée.')
                    self.chat.append("Une erreur est survenue. Veuillez vous référer à la fenêtre qui s'est affiché.")
                    self.chat.append("____________________________________________\n")
                    msg.setWindowTitle("Erreur !")
                    msg.exec()
                else: 
                    self.pseudo = "Client"
                    self.socket_client.send(self.pseudo.encode())
                    self.serverpseudo = self.socket_client.recv(1024).decode()
                    self.chat.append(f"Connecté sur {self.host}:{self.port} <-- {self.serverpseudo} !")
                    self.chat.append("____________________________________________\n")

    def envoi(self):
        try:
            comm = str(self.buttchos.currentText()) + str(self.commands.text())
            self.socket_client.send(comm.encode())
        except (socket.error, AttributeError) as err:
            print(err)
            print("151")
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'êtes connecté à aucun serveur.')
            msg.setWindowTitle("Erreur !")
            msg.exec()
        else:
            retour = self.socket_client.recv(1024).decode()
            textFormatted= f"{self.serverpseudo} > {retour}"
            self.chat.append(textFormatted)
    
    def oss(self):
        try:
            envoi = "OS"
            self.socket_client.send(envoi.encode())
        except (socket.error, AttributeError) as err:
            print(err)
            print("151")
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'êtes connecté à aucun serveur.')
            msg.setWindowTitle("Erreur !")
            msg.exec()
        else:
            retour = self.socket_client.recv(1024).decode()
            textFormatted= f"{self.serverpseudo} > {retour}"
            self.chat.append(textFormatted)
    
    def rams(self):
        try:
            envoi = "RAM"
            self.socket_client.send(envoi.encode())
        except (socket.error, AttributeError) as err:
            print(err)
            print("151")
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'êtes connecté à aucun serveur.')
            msg.setWindowTitle("Erreur !")
            msg.exec()
        else:
            retour = self.socket_client.recv(1024).decode()
            textFormatted= f"{self.serverpseudo} > {retour}"
            self.chat.append(textFormatted)

    def cpus(self):
        try:
            envoi = "CPU"
            self.socket_client.send(envoi.encode())
        except (socket.error, AttributeError) as err:
            print(err)
            print("151")
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'êtes connecté à aucun serveur.')
            msg.setWindowTitle("Erreur !")
            msg.exec()
        else:
            retour = self.socket_client.recv(1024).decode()
            textFormatted= f"{self.serverpseudo} > {retour}"
            self.chat.append(textFormatted)

    def ips(self):
        try:
            envoi = "IP"
            self.socket_client.send(envoi.encode())
        except (socket.error, AttributeError) as err:
            print(err)
            print("151")
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'êtes connecté à aucun serveur.')
            msg.setWindowTitle("Erreur !")
            msg.exec()
        else:
            retour = self.socket_client.recv(1024).decode()
            textFormatted= f"{self.serverpseudo} > {retour}"
            self.chat.append(textFormatted)

    def noms(self):
        try:
            envoi = "NOM"
            self.socket_client.send(envoi.encode())
        except (socket.error, AttributeError) as err:
            print(err)
            print("151")
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'êtes connecté à aucun serveur.')
            msg.setWindowTitle("Erreur !")
            msg.exec()
        else:
            retour = self.socket_client.recv(1024).decode()
            textFormatted= f"{self.serverpseudo} > {retour}"
            self.chat.append(textFormatted)

    def deconnection(self):
        try:
            bye = "disconnect"
            self.socket_client.send(bye.encode())
        except (socket.error, AttributeError):
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'êtes connecté à aucun serveur.')
            msg.setWindowTitle("Erreur !")
            msg.exec()
        else:
            self.socket_client.close()
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            msg = QMessageBox()
            msg.setText("Déconnecté avec succès.")
            msg.setWindowTitle("Déconnexion")
            msg.exec()
            self.chat.append("____________________________________________")

    def reset(self):
        try:
            bye = "reset"
            self.socket_client.send(bye.encode())
        except (socket.error, AttributeError):
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'êtes connecté à aucun serveur.')
            msg.setWindowTitle("Erreur !")
            msg.exec()
        else:
            print("Fermeture de la socket")
            try:
                self.socket_client.close()
                self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error as err:
                msg = QMessageBox()
                msg.setText("Erreur !")
                msg.setInformativeText(err)
                msg.setWindowTitle("Erreur !")
                msg.exec()
            else:
                self.chat.append("Vous avez été déconnecté du serveur.")
                msg = QMessageBox()
                msg.setText("Réinitialisé avec succès.")
                msg.setWindowTitle("Réinitialisation")
                msg.exec()
                self.chat.append("____________________________________________")

    def kill(self):
        try:
            bye = "kill"
            self.socket_client.send(bye.encode())
        except (socket.error, AttributeError):
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'êtes connecté à aucun serveur.')
            msg.setWindowTitle("Erreur !")
            msg.exec()
        else:
            self.socket_client.close()
            self.chat.append("Vous avez été déconnecté du serveur.")
            msg = QMessageBox()
            msg.setText("Tué avec succès.")
            msg.setWindowTitle("Kill")
            msg.exec()
            self.chat.append("____________________________________________")

    def closeEvent(self, _e: QCloseEvent):
        box = QMessageBox()
        box.setWindowTitle("Quitter ?")
        box.setText("Voulez vous quitter ?")
        box.addButton(QMessageBox.StandardButton.Yes)
        box.addButton(QMessageBox.StandardButton.No)

        ret = box.exec()

        if ret == QMessageBox.StandardButton.Yes.value:
            try:
                bye = "disconnect"
                self.socket_client.send(bye.encode())
            except (socket.error, AttributeError):
                pass
            QApplication.exit()
        else:
            _e.ignore()
    
app = QApplication.instance() 

if not app:
    app = QApplication(sys.argv)
    
sae32 = MainWindow()
sae32.show()

app.exec()
