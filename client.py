import sys
from PyQt5.QtWidgets import *
import threading
import requests

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
        self.commands = QTextEdit()
        self.commands.setMaximumHeight(25)
        self.envoyer = QPushButton("Envoyer")
        grid.addWidget(self.inf, 0, 0)
        grid.addWidget(self.buttos, 1,0)
        grid.addWidget(self.buttram, 1, 1)
        grid.addWidget(self.buttcpu, 1, 2)
        grid.addWidget(self.buttip, 1, 3)
        grid.addWidget(self.buttname, 1, 4)
        grid.addWidget(self.chat, 2, 0, 3, 5)
        grid.addWidget(self.commands, 5, 0, 1, 4)
        grid.addWidget(self.envoyer, 5, 4)
        widget.setLayout(grid)
        self.setWindowTitle("Gestionnaire de Serveurs")

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
        self.statusBar()
        menubar = self.menuBar()
        Menu = menubar.addMenu('&Menu')
        Menu.addAction(quitter)
        Menu.addAction(disconnect)
        Menu.addAction(kill)
        Menu.addAction(reset)
    
app = QApplication.instance() 

if not app:
    app = QApplication(sys.argv)
    
sae32 = MainWindow()
sae32.show()

app.exec_()
