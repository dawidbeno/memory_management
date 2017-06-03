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
        self.btnRunAll.clicked.connect(self.runAllSteps)
        self.btnStop.clicked.connect(self.stop)

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

        self.printMemory()


    def nextStep(self):
        step = self.getStep()
        if (step):
            self.getExecStepThread = controller.ExecuteStepThread(step)
            self.connect(self.getExecStepThread, SIGNAL('setPBT_SIG'), self.setPBT)
            self.connect(self.getExecStepThread, SIGNAL('appendST_SIG'), self.appendST)
            self.connect(self.getExecStepThread, SIGNAL('appendES_SIG'), self.appendES)
            self.connect(self.getExecStepThread, SIGNAL('setST_SIG'), self.setST)
            self.connect(self.getExecStepThread, SIGNAL('setMV_SIG'), self.setMV)
            self.connect(self.getExecStepThread, SIGNAL('appendMV_SIG'), self.appendMV)
            self.connect(self.getExecStepThread, SIGNAL('setPB_SIG'), self.setPB)
            self.getExecStepThread.start()


    def runAllSteps(self):
        self.test = self.getEntireTest()
        if self.test:
            self.getExecAllStepsThread = controller.ExecuteAllStepsThread(self.test)
            self.connect(self.getExecAllStepsThread, SIGNAL('setPBT_SIG'), self.setPBT)
            self.connect(self.getExecAllStepsThread, SIGNAL('appendST_SIG'), self.appendST)
            self.connect(self.getExecAllStepsThread, SIGNAL('appendES_SIG'), self.appendES)
            self.connect(self.getExecAllStepsThread, SIGNAL('setST_SIG'), self.setST)
            self.connect(self.getExecAllStepsThread, SIGNAL('setMV_SIG'), self.setMV)
            self.connect(self.getExecAllStepsThread, SIGNAL('appendMV_SIG'), self.appendMV)
            self.connect(self.getExecAllStepsThread, SIGNAL('setPB_SIG'), self.setPB)
            self.connect(self.getExecAllStepsThread, SIGNAL('setAT_SIG'), self.setAT)
            self.getExecAllStepsThread.start()

    def stop(self):
        self.getExecAllStepsThread.stopTesting()
        print "STOPPED"


#  ******* LOADING METHODS *******


    def getStep(self):
        wholeTest = self.tbActTest.toPlainText()
        step = wholeTest.split('\n')[0]
        stepLength = len(step)
        if (stepLength < 1):
            print "No step loaded"
            self.showStats()
            return
        wholeTest = wholeTest[(stepLength+1):]
        self.setAT(wholeTest)
        return step

    def getEntireTest(self):
        entireTest  = self.tbActTest.toPlainText()
        return entireTest

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
        self.printMemory()

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
        self.printMemory()

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

    def printMemory(self):
        self.getPrintMemThread = controller.PrintMemoryThread()
        self.connect(self.getPrintMemThread, SIGNAL('setMV_SIG'), self.setMV)
        self.connect(self.getPrintMemThread, SIGNAL('appendMV_SIG'), self.appendMV)
        self.connect(self.getPrintMemThread, SIGNAL('setPB_SIG'), self.setPB)
        self.getPrintMemThread.start()

    def showStats(self):
        self.getShowStatsThread = controller.ShowAllStatsThread()
        self.connect(self.getShowStatsThread, SIGNAL('setST_SIG'), self.setST)
        self.connect(self.getShowStatsThread, SIGNAL('appendST_SIG'), self.appendST)
        self.connect(self.getShowStatsThread, SIGNAL('setPB_SIG'), self.setPB)
        self.getShowStatsThread.start()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = View()
    form.show()
    app.exec_()

