import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from math import inf as infinity

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        startButton = QPushButton("Start")
        startButton.clicked.connect(self.startClicked)
        getBackButton = QPushButton("Get Back")
        getBackButton.clicked.connect(self.getBackClicked)

        buttonHbox = QHBoxLayout()
        buttonHbox.addStretch(1)
        buttonHbox.addWidget(startButton)
        buttonHbox.addWidget(getBackButton)

        xLabel = QLabel("x : ", self)
        self.xEdit = QLineEdit(self)
        yLabel = QLabel("y : ", self)
        self.yEdit = QLineEdit(self)
        addButton = QPushButton("Add")
        addButton.clicked.connect(self.addClicked)

        inputHBox = QHBoxLayout()
        inputHBox.addStretch(1)
        inputHBox.addWidget(xLabel)
        inputHBox.addWidget(self.xEdit)
        inputHBox.addWidget(yLabel)
        inputHBox.addWidget(self.yEdit)
        inputHBox.addWidget(addButton)

        tableLabel = QLabel("Table : ", self)
        self.tableEdit = QTextEdit()

        vBox = QVBoxLayout()
        vBox.stretch(1)
        vBox.addLayout(buttonHbox)
        vBox.addLayout(inputHBox)
        vBox.addWidget(tableLabel)
        vBox.addWidget(self.tableEdit)

        self.setLayout(vBox)

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle("¿À¸ñ")
        self.show()

    def startClicked(self):
        sender = self.sender()

    def getBackClicked(self):
        sender = self.sender()

    def addClicked(self):
        sender = self.sender()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())