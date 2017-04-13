import sys
from PyQt4 import QtGui

from src import form
import python_module.src.controller

app = QtGui.QApplication(sys.argv)
Form = QtGui.QWidget()
ui = form.Ui_Form()
ui.setupUi(Form)
Form.show()

#controller.init(ui)

sys.exit(app.exec_())




