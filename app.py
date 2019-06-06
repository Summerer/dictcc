# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

import sys
import tabulate

import dictcc


class Ui_MainWindow(object):

    def on_click(self):
        #popup = QMessageBox()
        #popup.setIcon(QMessageBox.Information)
        #popup.setText('Translating...')
        #popup.setWindowTitle("Status Change")
        #popup.exec()
        mytext = self.textEdit.toPlainText()
        #userInput = mytext.split()
        response = dictcc.request(mytext, 'de', 'en')
        data = dictcc.parse_response(response)
        #print(tabulate.tabulate(data, ['de', 'en'], tablefmt='orgtbl'))
        self.tableView.setText('')
        self.tableView.setText(tabulate.tabulate(data, ['de', 'en'], tablefmt='orgtbl'))




    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(690, 20, 88, 27))
        self.pushButton.setObjectName("pushButton")

        self.pushButton.setToolTip('Translate now')

        self.tableView = QtWidgets.QTextEdit(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 60, 771, 501))
        self.tableView.setObjectName("textResult")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(210, 10, 471, 41))
        self.textEdit.setObjectName("textEdit")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 20, 79, 27))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(110, 20, 79, 27))
        self.comboBox_2.setObjectName("comboBox_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.on_click)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Translate"))


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


