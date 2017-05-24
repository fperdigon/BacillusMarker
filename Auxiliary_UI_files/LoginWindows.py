# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginWindows.ui'
#
# Created: Wed Sep 30 12:46:02 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 240)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 200, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 60, 41, 16))
        self.label.setObjectName("label")
        self.Name_lineEdit = QtGui.QLineEdit(Dialog)
        self.Name_lineEdit.setGeometry(QtCore.QRect(60, 60, 241, 24))
        self.Name_lineEdit.setObjectName("Name_lineEdit")
        self.Marker_radioButton = QtGui.QRadioButton(Dialog)
        self.Marker_radioButton.setGeometry(QtCore.QRect(40, 130, 101, 21))
        self.Marker_radioButton.setObjectName("Marker_radioButton")
        self.Corrector_radioButton = QtGui.QRadioButton(Dialog)
        self.Corrector_radioButton.setGeometry(QtCore.QRect(180, 130, 101, 21))
        self.Corrector_radioButton.setObjectName("Corrector_radioButton")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Login Window", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.Marker_radioButton.setText(QtGui.QApplication.translate("Dialog", "Marker", None, QtGui.QApplication.UnicodeUTF8))
        self.Corrector_radioButton.setText(QtGui.QApplication.translate("Dialog", "Corrector", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

