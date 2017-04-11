import serial
import time
import sys
from PyQt4 import QtCore, QtGui
from gui import form

app = QtGui.QApplication(sys.argv)
Form = QtGui.QWidget()
ui = form.Ui_Form()
ui.setupUi(Form)
Form.show()




sys.exit(app.exec_())

