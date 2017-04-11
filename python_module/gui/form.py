# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1011, 675)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 20, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(180, 20, 121, 41))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 20, 121, 41))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(500, 20, 121, 41))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(660, 20, 121, 41))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 320, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.textBrowser = QtGui.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(10, 350, 191, 301))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.pushButton_5 = QtGui.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(220, 350, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(220, 430, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.textBrowser_2 = QtGui.QTextBrowser(Form)
        self.textBrowser_2.setGeometry(QtCore.QRect(10, 120, 991, 192))
        self.textBrowser_2.setObjectName(_fromUtf8("textBrowser_2"))
        self.textBrowser_3 = QtGui.QTextBrowser(Form)
        self.textBrowser_3.setGeometry(QtCore.QRect(430, 350, 551, 301))
        self.textBrowser_3.setObjectName(_fromUtf8("textBrowser_3"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(430, 320, 101, 17))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Testing app", None))
        self.label.setText(_translate("Form", "Load testing level :", None))
        self.pushButton.setText(_translate("Form", "1. level", None))
        self.pushButton_2.setText(_translate("Form", "2. level", None))
        self.pushButton_3.setText(_translate("Form", "3. level", None))
        self.pushButton_4.setText(_translate("Form", "4.level", None))
        self.label_2.setText(_translate("Form", "Memory visualization : ", None))
        self.label_3.setText(_translate("Form", "Actual test :", None))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.pushButton_5.setText(_translate("Form", "Next ", None))
        self.pushButton_6.setText(_translate("Form", "Run all", None))
        self.label_4.setText(_translate("Form", "Statistics :", None))


# if __name__ == "__main__":
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     Form = QtGui.QWidget()
#     ui = Ui_Form()
#     ui.setupUi(Form)
#     Form.show()
#     sys.exit(app.exec_())

