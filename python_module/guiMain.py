import sys
from PyQt4 import QtCore, QtGui

from src.form import Ui_Form
from src import controller

app = QtGui.QApplication(sys.argv)
Form = QtGui.QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()

controller.init(ui)


sys.exit(app.exec_())