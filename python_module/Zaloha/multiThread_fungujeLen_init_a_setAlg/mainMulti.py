# multiThread
from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL
import sys
import form
import controller
import time



class View(QtGui.QMainWindow, form.Ui_Form):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.btnLoadLvl1.clicked.connect(self.load_1)
        self.btnLoadLvl2.clicked.connect(self.load_2)
        self.btnLoadLvl3.clicked.connect(self.load_3)
        self.btnLoadLvl4.clicked.connect(self.load_4)
        self.btnAllStats.clicked.connect(self.showStats)
        self.btnSetBest.clicked.connect(self.setAlgBest)
        self.btnSetWorst.clicked.connect(self.setAlgWorst)
        self.btnNextStep.clicked.connect(self.nextStep)

        self.getInitThread = controller.initThread()
        self.connect(self.getInitThread, SIGNAL('appendST_SIG'), self.appendST)
        self.getInitThread.start()

        while not self.getInitThread.isFinished():
            time.sleep(2)

        self.getSetAlgThread = controller.SetAlgorithmThread(controller.BEST)
        self.connect(self.getSetAlgThread, SIGNAL('setST_SIG'), self.setST)
        self.connect(self.getSetAlgThread, SIGNAL('setAT_SIG'), self.setAT)
        self.connect(self.getSetAlgThread, SIGNAL('setES_SIG'), self.appendES)
        self.connect(self.getSetAlgThread, SIGNAL('setPBT_SIG'), self.setPBT)
        self.connect(self.getSetAlgThread, SIGNAL('appendST_SIG'), self.appendST)
        self.getSetAlgThread.start()
        while not self.getSetAlgThread.isFinished():
            time.sleep(1)
        self.setAlg(controller.BEST)



    def nextStep(self):
        step = self.getStep()
        if(step):
            controller.nextStep(self, step)

    def showStats(self):
        controller.showAllStats(self)



#  ******* LOADING METHODS *******


    def getStep(self):
        wholeTest = self.tbActTest.toPlainText()
        step = wholeTest.split('\n')[0]
        stepLength = len(step)
        if (stepLength < 1):
            print "No step loaded"
            controller.showAllStats(self)
            return
        wholeTest = wholeTest[(stepLength+1):]
        self.setAT(wholeTest)
        return step

    def load_1(self):
        test = controller.load_1()
        self.setAT(test)
        self.tbExecSteps.setText("")

    def load_2(self):
        test = controller.load_2()
        self.setAT(test)
        self.tbExecSteps.setText("")

    def load_3(self):
        test = controller.load_3()
        self.setAT(test)
        self.tbExecSteps.setText("")

    def load_4(self):
        test = controller.load_4()
        self.setAT(test)
        self.tbExecSteps.setText("")

    def setAlgBest(self):
        self.getSetAlgThread = controller.SetAlgorithmThread(controller.BEST)
        self.connect(self.getSetAlgThread, SIGNAL('setST_SIG'), self.setST)
        self.connect(self.getSetAlgThread, SIGNAL('setAT_SIG'), self.setAT)
        self.connect(self.getSetAlgThread, SIGNAL('setES_SIG'), self.appendES)
        self.connect(self.getSetAlgThread, SIGNAL('setPBT_SIG'), self.setPBT)
        self.connect(self.getSetAlgThread, SIGNAL('appendST_SIG'), self.appendST)
        self.getSetAlgThread.start()
        while not self.getSetAlgThread.isFinished():
            time.sleep(1)
        self.setAlg(controller.BEST)

    def setAlgWorst(self):
        self.getSetAlgThread = controller.SetAlgorithmThread(controller.WORST)
        self.connect(self.getSetAlgThread, SIGNAL('setST_SIG'), self.setST)
        self.connect(self.getSetAlgThread, SIGNAL('setAT_SIG'), self.setAT)
        self.connect(self.getSetAlgThread, SIGNAL('setES_SIG'), self.appendES)
        self.connect(self.getSetAlgThread, SIGNAL('setPBT_SIG'), self.setPBT)
        self.connect(self.getSetAlgThread, SIGNAL('appendST_SIG'), self.appendST)
        self.getSetAlgThread.start()
        while not self.getSetAlgThread.isFinished():
            time.sleep(1)
        self.setAlg(controller.WORST)

    def getNumOfRemainingSteps(self):
        test = self.tbActTest.toPlainText()
        steps = test.split('\n')
        return len(steps)



    #  ******* PRINT METHODS  *********

    def setAlg(self, alg):
        if(alg == controller.BEST):
            self.lbActAlg.setText("BEST")
        elif(alg == controller.WORST):
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



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = View()
    form.show()
    app.exec_()

