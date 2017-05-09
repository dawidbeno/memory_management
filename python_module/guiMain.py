import sys
from PyQt4 import QtGui

from src.form import Ui_Form
from src import controller

app = QtGui.QApplication(sys.argv)
Form = QtGui.QWidget()
ui = Ui_Form()
ui.setupUi(Form)

controller.init(ui)


Form.show()

sys.exit(app.exec_())


# class MainGuiClass(QtGui.QMainWindow, form.Ui_Form):
#     def __init__(self, parent = None):
#         super(MainGuiClass, self).__init__(parent)
#         self.setupUi(self)
#         self.threadClass = ThreadClass()
#         self.threadClass.start()
#
#
#
#
#
# class ThreadClass(QtCore.QThread):
#     def __init__(self, parent = None):
#         super(ThreadClass, self).__init__(parent)
#
#     def conInit(self, ui):
#         controller.init(ui)
#
#
# if __name__ == '__main__':
#     a = QtGui.QApplication(sys.argv)
#     app = MainGuiClass()
#     app.show()
#     a.exec_()
#






