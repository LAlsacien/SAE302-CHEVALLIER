import sys

from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QTextEdit, QPushButton, QScrollArea


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.lista = ["one", "two", "abcdefghijklmn", "zxyw", "xyxyxyxyx"]

        self.widget = QWidget(self)
        self.layout = QVBoxLayout(self.widget)

        self.area = QScrollArea(self)
        self.area.resize(400,300)
        self.area.setWidget(self.widget)
        self.area.setWidgetResizable(True)

        self.plain = QTextEdit(self)
        self.plain.move(0,305)
        self.plain.resize(400,50)

        self.boton = QPushButton(self)
        self.boton.move(0,360)
        self.boton.setText("Press")

        self.boton.clicked.connect(self.Test)

    def Test(self):
        for i in self.lista:
            text = QTextEdit(self)
            text.document().setPlainText(i)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Main()
    m.show()
    m.resize(600, 400)
    sys.exit(app.exec_())