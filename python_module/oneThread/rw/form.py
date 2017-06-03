# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import src.controller
import time


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
        Form.resize(1087, 673)
        self.lbLTL = QtGui.QLabel(Form)
        self.lbLTL.setGeometry(QtCore.QRect(10, 20, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lbLTL.setFont(font)
        self.lbLTL.setObjectName(_fromUtf8("lbLTL"))
        self.btnLoadLvl1 = QtGui.QPushButton(Form)
        self.btnLoadLvl1.setGeometry(QtCore.QRect(180, 20, 91, 41))
        self.btnLoadLvl1.setObjectName(_fromUtf8("btnLoadLvl1"))
        self.btnLoadLvl2 = QtGui.QPushButton(Form)
        self.btnLoadLvl2.setGeometry(QtCore.QRect(280, 20, 101, 41))
        self.btnLoadLvl2.setObjectName(_fromUtf8("btnLoadLvl2"))
        self.btnLoadLvl3 = QtGui.QPushButton(Form)
        self.btnLoadLvl3.setGeometry(QtCore.QRect(390, 20, 101, 41))
        self.btnLoadLvl3.setObjectName(_fromUtf8("btnLoadLvl3"))
        self.btnLoadLvl4 = QtGui.QPushButton(Form)
        self.btnLoadLvl4.setGeometry(QtCore.QRect(500, 20, 101, 41))
        self.btnLoadLvl4.setObjectName(_fromUtf8("btnLoadLvl4"))
        self.lbMV = QtGui.QLabel(Form)
        self.lbMV.setGeometry(QtCore.QRect(380, 80, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lbMV.setFont(font)
        self.lbMV.setObjectName(_fromUtf8("lbMV"))
        self.lbAT = QtGui.QLabel(Form)
        self.lbAT.setGeometry(QtCore.QRect(760, 80, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lbAT.setFont(font)
        self.lbAT.setObjectName(_fromUtf8("lbAT"))
        self.tbActTest = QtGui.QTextBrowser(Form)
        self.tbActTest.setGeometry(QtCore.QRect(750, 110, 151, 351))
        self.tbActTest.setObjectName(_fromUtf8("tbActTest"))
        self.btnNextStep = QtGui.QPushButton(Form)
        self.btnNextStep.setGeometry(QtCore.QRect(750, 540, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btnNextStep.setFont(font)
        self.btnNextStep.setObjectName(_fromUtf8("btnNextStep"))
        self.btnRunAll = QtGui.QPushButton(Form)
        self.btnRunAll.setGeometry(QtCore.QRect(750, 600, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btnRunAll.setFont(font)
        self.btnRunAll.setObjectName(_fromUtf8("btnRunAll"))
        self.tbMemVisual = QtGui.QTextBrowser(Form)
        self.tbMemVisual.setGeometry(QtCore.QRect(380, 110, 341, 541))
        self.tbMemVisual.setObjectName(_fromUtf8("tbMemVisual"))
        self.tbStats = QtGui.QTextBrowser(Form)
        self.tbStats.setGeometry(QtCore.QRect(10, 110, 341, 441))
        self.tbStats.setObjectName(_fromUtf8("tbStats"))
        self.lbStats = QtGui.QLabel(Form)
        self.lbStats.setGeometry(QtCore.QRect(10, 90, 101, 17))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lbStats.setFont(font)
        self.lbStats.setObjectName(_fromUtf8("lbStats"))
        self.lbActAlg = QtGui.QLabel(Form)
        self.lbActAlg.setGeometry(QtCore.QRect(650, 80, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lbActAlg.setFont(font)
        self.lbActAlg.setObjectName(_fromUtf8("lbActAlg"))
        self.btnSetBest = QtGui.QPushButton(Form)
        self.btnSetBest.setGeometry(QtCore.QRect(620, 10, 99, 27))
        self.btnSetBest.setObjectName(_fromUtf8("btnSetBest"))
        self.btnSetWorst = QtGui.QPushButton(Form)
        self.btnSetWorst.setGeometry(QtCore.QRect(620, 40, 99, 27))
        self.btnSetWorst.setObjectName(_fromUtf8("btnSetWorst"))
        self.lbES = QtGui.QLabel(Form)
        self.lbES.setGeometry(QtCore.QRect(920, 80, 131, 17))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lbES.setFont(font)
        self.lbES.setObjectName(_fromUtf8("lbES"))
        self.tbExecSteps = QtGui.QTextBrowser(Form)
        self.tbExecSteps.setGeometry(QtCore.QRect(920, 110, 151, 351))
        self.tbExecSteps.setObjectName(_fromUtf8("tbExecSteps"))
        self.btnStop = QtGui.QPushButton(Form)
        self.btnStop.setGeometry(QtCore.QRect(890, 600, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btnStop.setFont(font)
        self.btnStop.setObjectName(_fromUtf8("btnStop"))
        self.pbMemUtil = QtGui.QProgressBar(Form)
        self.pbMemUtil.setGeometry(QtCore.QRect(10, 590, 341, 41))
        self.pbMemUtil.setProperty("value", 24)
        self.pbMemUtil.setObjectName(_fromUtf8("pbMemUtil"))
        self.lbMemUtil = QtGui.QLabel(Form)
        self.lbMemUtil.setGeometry(QtCore.QRect(10, 560, 211, 17))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lbMemUtil.setFont(font)
        self.lbMemUtil.setObjectName(_fromUtf8("lbMemUtil"))
        self.pbTest = QtGui.QProgressBar(Form)
        self.pbTest.setGeometry(QtCore.QRect(750, 492, 321, 41))
        self.pbTest.setProperty("value", 24)
        self.pbTest.setObjectName(_fromUtf8("pbTest"))
        self.lbTestProgres = QtGui.QLabel(Form)
        self.lbTestProgres.setGeometry(QtCore.QRect(750, 470, 211, 17))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lbTestProgres.setFont(font)
        self.lbTestProgres.setObjectName(_fromUtf8("lbTestProgres"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.btnLoadLvl1, QtCore.SIGNAL(_fromUtf8("clicked()")), self.loadTest_1)
        QtCore.QObject.connect(self.btnLoadLvl2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.loadTest_2)
        QtCore.QObject.connect(self.btnLoadLvl3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.loadTest_3)
        QtCore.QObject.connect(self.btnLoadLvl4, QtCore.SIGNAL(_fromUtf8("clicked()")), self.loadTest_4)

        QtCore.QObject.connect(self.btnNextStep, QtCore.SIGNAL(_fromUtf8("clicked()")), self.nextStep)
        QtCore.QObject.connect(self.btnRunAll, QtCore.SIGNAL(_fromUtf8("clicked()")), self.allSteps)

        QtCore.QObject.connect(self.btnSetBest, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setAlgBest)
        QtCore.QObject.connect(self.btnSetWorst, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setAlgWorst)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.lbLTL.setText(_translate("Form", "Load testing level :", None))
        self.btnLoadLvl1.setText(_translate("Form", "1. level", None))
        self.btnLoadLvl2.setText(_translate("Form", "2. level", None))
        self.btnLoadLvl3.setText(_translate("Form", "3. level", None))
        self.btnLoadLvl4.setText(_translate("Form", "4.level", None))
        self.lbMV.setText(_translate("Form", "Memory visualization : ", None))
        self.lbAT.setText(_translate("Form", "Actual test :", None))
        self.tbActTest.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.btnNextStep.setText(_translate("Form", "Next step", None))
        self.btnRunAll.setText(_translate("Form", "Run all", None))
        self.lbStats.setText(_translate("Form", "Statistics :", None))
        self.lbActAlg.setText(_translate("Form", "Act alg", None))
        self.btnSetBest.setText(_translate("Form", "BEST FIT", None))
        self.btnSetWorst.setText(_translate("Form", "WORST FIT", None))
        self.lbES.setText(_translate("Form", "Executed steps :", None))
        self.btnStop.setText(_translate("Form", "Stop", None))
        self.lbMemUtil.setText(_translate("Form", "Memory utilization :", None))
        self.lbTestProgres.setText(_translate("Form", "Test progress :", None))



    def nextStep(self):
        step = self.getStep()
        if(step):
            src.controller.nextStep(self, step)


    def allSteps(self):
        numOfRemainingSteps = self.getNumOfRemainingSteps()
        for x in range(0, numOfRemainingSteps-2):  # minus 2 because of first and last line in test file
            self.nextStep()
            time.sleep(1)


    # ********* LOADING METHODS  ***********

    def loadTest_1(self):
        test = src.controller.load_1(self)
        self.setAT(test)
        self.tbExecSteps.setText("")

    def loadTest_2(self):
        test = src.controller.load_2(self)
        self.setAT(test)
        self.tbExecSteps.setText("")

    def loadTest_3(self):
        test = src.controller.load_3(self)
        self.setAT(test)
        self.tbExecSteps.setText("")

    def loadTest_4(self):
        test = src.controller.load_4(self)
        self.setAT(test)
        self.tbExecSteps.setText("")

    def getStep(self):
        wholeTest = self.tbActTest.toPlainText()
        step = wholeTest.split('\n')[0]
        stepLength = len(step)
        if (stepLength < 1):
            print "No step loaded"
            src.controller.showAllStats(self)
            return
        wholeTest = wholeTest[(stepLength+1):]
        self.setAT(wholeTest)
        return step

    def getNumOfRemainingSteps(self):
        test = self.tbActTest.toPlainText()
        steps = test.split('\n')
        return len(steps)

    def setAlgBest(self):
        src.controller.setAlgorithm(self, src.controller.BEST)

    def setAlgWorst(self):
        src.controller.setAlgorithm(self, src.controller.WORST)




    # ******  PRINT METHODS  *********

    def setAlg(self, alg):
        if(alg == src.controller.BEST):
            self.lbActAlg.setText("BEST")
        elif(alg == src.controller.WORST):
            self.lbActAlg.setText("WORST")
        else:
            self.lbActAlg.setText("BAD")
            self.setST("FATAL ERROR: Setting algorithm failed")

    def appendMV(self, str):
        self.tbMemVisual.append(str)

    def setMV(self, str):
        self.tbMemVisual.setText(str)

    def appendST(self, str):
        self.tbStats.append(str)

    def setST(self, str):
        self.tbStats.setText(str)

    def setAT(self, str):
        self.tbActTest.setText(str)

    def appendPB(self, str):
        actVal = self.pbMemUtil.value()
        actVal += int(str)
        self.pbMemUtil.setValue(actVal)

    def setPB(self,str):
        val = round(float(str))
        self.pbMemUtil.setValue(val)

    def setES(self, str):
        self.tbExecSteps.setText(str)

    def appendES(self, str):
        self.tbExecSteps.append(str)

    def setPBT(self, str):
        str = round(float(str))
        self.pbTest.setValue(int(str))





if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

