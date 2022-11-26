import sys
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        grid = QGridLayout()
        widget.setLayout(grid)

app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
    
sae32 = MainWindow()
sae32.show()

app.exec_()