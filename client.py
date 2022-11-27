import sys
from PyQt5.QtWidgets import *
import socket
import requests
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
        self.buttram = QPushButton("RAM")
        self.buttcpu = QPushButton("CPU")
        self.buttip = QPushButton("IP")
        self.buttname = QPushButton("Nom")
        self.chat = QTextEdit()
        self.commands = QLineEdit()
        self.commands.setMaximumHeight(25)
        self.envoyer = QPushButton("Envoyer")
        self.envoyer.clicked.connect(self.envoi)
        self.conn = QLabel("IP du Serveur :")
        self.ip = QLineEdit()
        self.conn2 = QPushButton("Se connecter")
        self.conn2.clicked.connect(self.connect)
        self.ip.setMaximumHeight(25)
        grid.addWidget(self.inf, 0, 0)
        grid.addWidget(self.buttos, 1,0)
        grid.addWidget(self.buttram, 1, 1)
        grid.addWidget(self.buttcpu, 1, 2)
        grid.addWidget(self.buttip, 1, 3)
        grid.addWidget(self.buttname, 1, 4)
        grid.addWidget(self.chat, 2, 0, 3, 5)
        grid.addWidget(self.commands, 5, 0, 1, 4)
        grid.addWidget(self.envoyer, 5, 4)
        grid.addWidget(self.conn, 6, 0)
        grid.addWidget(self.ip, 6, 1, 1, 2)
        grid.addWidget(self.conn2, 6, 3)
        widget.setLayout(grid)
        self.setWindowTitle("Gestionnaire de Serveurs")
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        quitter.triggered.connect(qApp.quit)
        disconnect.triggered.connect(self.deconnection)
        self.statusBar()
        menubar = self.menuBar()
        Menu = menubar.addMenu('&Menu')
        Menu.addAction(quitter)
        Menu.addAction(disconnect)
        Menu.addAction(kill)
        Menu.addAction(reset)

    def connect(self):
        try:
            host = ipaddress.ip_address(self.ip.text())
        except ValueError:
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'avez pas entrée une IP correcte.')
            msg.setWindowTitle("Erreur !")
            msg.exec_()
        else:
            try:
                host = str(self.ip.text())
                self.socket_client.connect((host, 10000))
            except socket.error:
                msg = QMessageBox()
                msg.setText("Erreur !")
                msg.setInformativeText('Connexion impossible ou refusée.')
                msg.setWindowTitle("Erreur !")
                msg.exec_()
            else:
                pseudo, entrer = QInputDialog.getText(self, "Connexion réussie.", "Veuillez entrer votre pseudo :", QLineEdit.Normal, "")
                if entrer:
                    pseudo = pseudo
                self.socket_client.send(pseudo.encode())
                serverpseudo = self.socket_client.recv(1024).decode()
    
    def envoi(self):
        try:
            envoi = self.commands.text()
            self.socket_client.send(envoi.encode())
        except socket.error:
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'êtes connecté à aucun serveur.')
            msg.setWindowTitle("Erreur !")
            msg.exec_()
        else:
            pass

    def deconnection(self):
        try:
            bye = "bye"
            self.socket_client.send(bye.encode())
        except socket.error:
            msg = QMessageBox()
            msg.setText("Erreur !")
            msg.setInformativeText('Vous n\'êtes connecté à aucun serveur.')
            msg.setWindowTitle("Erreur !")
            msg.exec_()
        else:
            self.socket_client.close()
            msg = QMessageBox()
            msg.setText("Déconnecté avec succès.")
            msg.setWindowTitle("Déconnexion")
            msg.exec_()

app = QApplication.instance() 

if not app:
    app = QApplication(sys.argv)
    
sae32 = MainWindow()
sae32.show()

app.exec_()
