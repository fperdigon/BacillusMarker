# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UsersInfo.ui'
#
# Created: Wed Sep 30 19:36:33 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(504, 240)
        self.Log_tableWidget = QtGui.QTableWidget(Dialog)
        self.Log_tableWidget.setGeometry(QtCore.QRect(10, 20, 481, 201))
        self.Log_tableWidget.setObjectName("Log_tableWidget")
        self.Log_tableWidget.setColumnCount(2)
        self.Log_tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.Log_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.Log_tableWidget.setHorizontalHeaderItem(1, item)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Users Info", None, QtGui.QApplication.UnicodeUTF8))
        self.Log_tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Dialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.Log_tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Dialog", "User Type", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

