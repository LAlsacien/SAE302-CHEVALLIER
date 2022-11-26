import sys
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import *
import threading
import requests

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.chat = []
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        self.client = QScrollArea(self)
        self.client.resize(400,300)
        self.client.setWidget(self.widget)
        self.client.setWidgetResizable(True)

        self.commands = QTextEdit(self)
        self.commands.move(0,305)
        self.commands.resize(400,50)

        self.button = QPushButton(self)
        self.button.move(0,360)
        self.button.setText("Envoyer")
        self.button.clicked.connect(self.envoi)

        
    def envoi(self):
        envoi = self.commands.text()
        text = QTextEdit(self)
        text.document().setPlainText()
        
        font = text.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        textSize = fontMetrics.size(0, text.toPlainText())

        w = textSize.width() + 10
        h = textSize.height() + 10
        text.setMinimumSize(w, h)
        text.setMaximumSize(w, h)
        text.resize(w, h)

        text.setReadOnly(True)
        self.layout.addWidget(text)

app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
    
sae32 = MainWindow()
sae32.resize(600, 400)
sae32.show()

app.exec_()
