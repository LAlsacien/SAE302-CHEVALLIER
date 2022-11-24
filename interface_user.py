import sys
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
root = QWidget()
root.resize(250,250)
root.setWindowTitle("PyQT App")
grid = QGridLayout()
BTN1 = QPushButton("Disconnect")
BTN2 = QPushButton("Kill")
BTN3 = QPushButton("Reset")
grid.addWidget(BTN1, 0, 0)
grid.addWidget(BTN2, 0, 1)
grid.addWidget(BTN3, 0, 2)
root.setLayout(grid)

root.show()

if __name__ == '__main__':
    sys.exit(app.exec_())
