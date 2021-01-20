import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit, QCheckBox


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 550, 300)
        self.setWindowTitle('SKATT тренажер')

        self.edit1 = QCheckBox(self)
        self.edit1.setText('edit1')
        self.edit1.move(10, 10)
        self.edit1.connect(self.run)

        self.edit2 = QCheckBox(self)
        self.edit2.setText('edit2')
        self.edit2.move(10, 30)
        self.edit2.connect(self.run)

        self.edit3 = QCheckBox(self)
        self.edit3.setText('edit3')
        self.edit3.move(10, 50)
        self.edit3.connect(self.run)

        self.edit4 = QCheckBox(self)
        self.edit4.setText('edit4')
        self.edit4.move(10, 70)
        self.edit4.clicked.connect(self.run)

        self.pole1 = QLineEdit('поле edit4', self)
        self.pole1.setEnabled(False)
        self.pole1.move(70, 10)
        self.pole1.resize(100, 20)

        self.pole2 = QLineEdit('поле edit2', self)
        self.pole2.setEnabled(False)
        self.pole2.move(70, 30)
        self.pole2.resize(100, 20)

        self.pole3 = QLineEdit('поле edit3', self)
        self.pole3.setEnabled(False)
        self.pole3.move(70, 50)
        self.pole3.resize(100, 20)

        self.pole4 = QLineEdit('поле edit4', self)
        self.pole4.setEnabled(False)
        self.pole4.move(70, 70)
        self.pole4.resize(100, 20)


    def run(self):
        self.pole1.hide()
        self.pole2.hide()
        self.pole3.hide()
        self.pole4.hide()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
