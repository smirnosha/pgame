import sys

from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtWidgets import QMainWindow
from random import randint
from PyQt5.QtCore import Qt


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.x = 0
        self.y = 0
        self.right = False

    def initUI(self):
        self.setGeometry(300, 300, 600, 600)

        self.btn = QPushButton('Кнопка', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(100, 100)
        self.btn.resize(160, 50)
        self.btn.clicked.connect(self.start)

    def mouseMoveEvent(self, event):
        self.x = event.x
        self.y = event.y

    def mousePressEvent(self, event):
        self.x = event.x
        self.y = event.y
        if (event.button() == Qt.RightButton):
            self.right = True
        self.repaint()

    def start(self):
        a = randint(0, 600)
        b = randint(0, 600)
        if self.right:
            self.x = a
            self.y = b
            self.btn.move(self.x(), self.y())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
