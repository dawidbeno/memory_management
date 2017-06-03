# multiThread
import serial
import time
from PyQt4.QtCore import QThread, SIGNAL


TEST_DIR = "/Users/dejvid/Codes/memory_management/tests/"
serialComm = None

BEST = 'b'
WORST = 'w'


ALGORITHM = BEST
ADDRS = [None]

MEM_BLOCK_SIZE = 6
remainingMem = 0
wholeMem = 4096

numOfAllocs = 0
sucAllocs = 0

numOfFrees = 0
sucFrees = 0

numOfReallocs = 0
sucReallocs = 0

bestAllocTime = 9999
worstAllocTime = 0
countAllocTime = 0

bestFreeTime = 9999
worstFreeTime = 0
countFreeTime = 0

bestReallocTime = 9999
worstReallocTime = 0
countReallocTime = 0

maxAllocBlock = 0
minAllocBlock = 5000
sizeCount = 0
averageAllocBlock = 5000
numOfExtFragFail = 0

maxFreeBlock = 0
minFreeBlock = 5000
averageFreeBlock = 5000
numOfUnusable = 0
numOfFreeBlocks = 0

wholeTime = 0

stepNum = 0
numOfSteps = 0

numOfBlocks = 3

internalFragment = 0

numAllocFails = 0

# Arduino uses BEST fit as default algorithm


# *****************************************
#
#            INIT FUNCTIONS
#
# *****************************************


class initThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def execInit(self):
        global serialComm
        try:
            serialComm = serial.Serial('/dev/tty.usbmodem1421', 9600)
            time.sleep(1)
            var = serialComm.readline()
            serialComm.write(b'i')
            while 1:
                time.sleep(1)
                var = serialComm.readline()
                if (var == "INIT\r\n"):
                    print "init successful"
                    self.emit(SIGNAL('appendST_SIG'), 'Init successful')
                    # setalg
                    break
                else:
                    self.emit(SIGNAL('appendST_SIG'), 'waiting for init ...')
                    print "waiting for init ..."
        except Exception:
            print "Serial port not found"
            self.emit(SIGNAL('appendST_SIG'), 'FATAL ERROR: Serial port not found. Communication will not work')




    def run(self):
        self.execInit()


class SetAlgorithmThread(QThread):
    def __init__(self, algType):
        QThread.__init__(self)
        self.algType = algType

    def __del__(self):
        self.wait()

    def setAlgorithm(self, algType):
        global serialComm, BEST, WORST, ALGORITHM
        global numOfAllocs, numOfFrees, numOfReallocs
        global sucAllocs, sucFrees, sucReallocs
        global bestFreeTime, bestReallocTime, bestAllocTime
        global worstFreeTime, worstReallocTime, worstAllocTime
        global countAllocTime, countFreeTime, countReallocTime
        global maxAllocBlock, minAllocBlock, averageAllocBlock, sizeCount
        global wholeTime, stepNum, numOfSteps
        global internalFragment, numOfExtFragFail
        global numOfBlocks
        global maxFreeBlock, minFreeBlock, averageFreeBlock, numOfUnusable, numOfFreeBlocks
        numOfAllocs = 0
        numOfFrees = 0
        numOfReallocs = 0
        sucAllocs = 0
        sucFrees = 0
        sucReallocs = 0
        bestAllocTime = 9999
        worstAllocTime = 0
        countAllocTime = 0
        bestFreeTime = 9999
        worstFreeTime = 0
        countFreeTime = 0
        bestReallocTime = 99999
        worstReallocTime = 0
        countReallocTime = 0
        maxAllocBlock = 0
        minAllocBlock = 9999
        averageAllocBlock = 9999
        sizeCount = 0
        wholeTime = 0
        stepNum = 0
        numOfExtFragFail = 0
        internalFragment = 0
        maxFreeBlock = 0
        minFreeBlock = 5000
        averageFreeBlock = 5000
        numOfUnusable = 0
        numOfFreeBlocks = 0
        numOfStep = 0
        numOfBlocks = 3
        self.emit(SIGNAL('setST_SIG'), '')
        self.emit(SIGNAL('setAT_SIG'), '')
        self.emit(SIGNAL('setES_SIG'), '')
        self.emit(SIGNAL('setPBT_SIG'), 0)
        if (algType == BEST):
            serialComm.write(b'b')
            while True:
                var = serialComm.readline()
                if (var.__contains__("Alg changed to:")):
                    var2 = var.split(':')[1]
                    var = var2[0]
                    if (var == 'b'):
                        ALGORITHM = "BEST"
                        print "Set alg to BEST"
                        self.emit(SIGNAL('appendST_SIG'), 'Algorithm is set to BEST')
                        #printMemory(ui)
                        break
                print "waiting to set algorithm ..."
                self.emit(SIGNAL('appendST_SIG'), 'waiting to set algorithm ...')
                time.sleep(0.1)

        elif (algType == WORST):
            serialComm.write(b'w')
            while True:
                var = serialComm.readline()
                if (var.__contains__("Alg changed to:")):
                    var2 = var.split(':')[1]
                    var = var2[0]
                    if (var == 'w'):
                        ALGORITHM = "WORST"
                        print "Set alg to WORST"
                        self.emit(SIGNAL('appendST_SIG'), 'Algorithm is set to WORST')
                        #printMemory(ui)
                        break
                print "waiting to set algorithm ..."
                self.emit(SIGNAL('appendST_SIG'), 'waiting to set algorithm ...')
                time.sleep(0.1)

        else:
            print "Bad type of algorithm"
            print "Type \"help\" for more info"


    def run(self):
        global BEST, WORST
        if self.algType == BEST:
            self.setAlgorithm(BEST)
        else:
            self.setAlgorithm(WORST)





# ***************************************
#
#            LOAD FUNCTIONS
#
# ***************************************

def load_1():
    global TEST_DIR, ADDRS, stepNum, numOfSteps
    stepNum = 0
    try:
        file = open(TEST_DIR+"level_1", "r").read()
        numOfSteps = sum(1 for line in open(TEST_DIR+"level_1"))
        numOfSteps -= 1
    except Exception:
            print "File not found"
            return
    ptrnum = file.split('\n')[0]
    ptrnumLen = len(ptrnum)
    file = file[(ptrnumLen+1):]
    ptrnum = ptrnum.split(' ')[1]

    ptrnum = int(float(ptrnum))
    ADDRS = [None] * ptrnum

    return file

def load_2():
    global TEST_DIR, ADDRS, stepNum, numOfSteps
    stepNum = 0
    try:
        file = open(TEST_DIR+"level_2", "r").read()
        numOfSteps = sum(1 for line in open(TEST_DIR + "level_2"))
        numOfSteps -= 1
    except Exception:
            print "File not found"
            return
    ptrnum = file.split('\n')[0]
    ptrnumLen = len(ptrnum)
    file = file[(ptrnumLen+1):]
    ptrnum = ptrnum.split(' ')[1]

    ptrnum = int(float(ptrnum))
    ADDRS = [None] * ptrnum

    return file

def load_3():
    global TEST_DIR, ADDRS, stepNum, numOfSteps
    stepNum = 0
    try:
        file = open(TEST_DIR+"level_3", "r").read()
        numOfSteps = sum(1 for line in open(TEST_DIR + "level_3"))
        numOfSteps -= 1
    except Exception:
            print "File not found"
            return
    ptrnum = file.split('\n')[0]
    ptrnumLen = len(ptrnum)
    file = file[(ptrnumLen+1):]
    ptrnum = ptrnum.split(' ')[1]

    ptrnum = int(float(ptrnum))
    ADDRS = [None] * ptrnum

    return file

def load_4():
    global TEST_DIR, ADDRS, stepNum, numOfSteps
    stepNum = 0
    try:
        file = open(TEST_DIR+"level_4", "r").read()
        numOfSteps = sum(1 for line in open(TEST_DIR + "level_4"))
        numOfSteps -= 1
    except Exception:
            print "File not found"
            return
    ptrnum = file.split('\n')[0]
    ptrnumLen = len(ptrnum)
    file = file[(ptrnumLen+1):]
    ptrnum = ptrnum.split(' ')[1]

    ptrnum = int(float(ptrnum))
    ADDRS = [None] * ptrnum

    return file




# *********************************************
#
#              EXECUTE FUNCTIONS
#
# *********************************************


class ExecuteStepThread(QThread):
    def __init__(self, step):
        QThread.__init__(self)
        self.step = step

    def __del__(self):
        self.wait()

    def nextStep(self, step):
        global stepNum, numOfSteps
        stepNum += 1
        p = ((float(stepNum) / float(numOfSteps)) * 100)
        self.emit(SIGNAL('setPBT_SIG'), p)
        self.emit(SIGNAL('appendST_SIG'), 'NEXT STEP')
        self.runStep(step)
        time.sleep(1)
        self.printMem()
        self.emit(SIGNAL('appendES_SIG'), step)
        if (stepNum % 5 == 0):
            self.exportStatsToFile()


    def runStep(self, step):
        global numOfAllocs, numOfFrees, numOfReallocs
        self.emit(SIGNAL('setST_SIG'), '')
        type = step.split(' ')[0]
        if(type == "alloc"):
            numOfAllocs += 1
            self.allocateMem(step)
        if(type == "free"):
            numOfFrees += 1
            self.freeMem(step)
        if(type == "realloc"):
            numOfReallocs += 1
            self.reallocMem(step)


    def allocateMem(self, step):
        global serialComm
        global bestAllocTime, worstAllocTime, sucAllocs, countAllocTime
        global maxAllocBlock, minAllocBlock, averageAllocBlock, sizeCount
        global stepNum, numOfExtFragFail
        print "\n **** Start test allocation **** StepNum:"+str(stepNum)
        self.emit(SIGNAL('appendST_SIG'), "Request type:                   Allocation\n")
        size = step.split(' ')[1]
        size = str(size)
        serialComm.write(b'a')
        if (len(size) == 1):
            serialComm.write(b'1')
        elif (len(size) == 2):
            serialComm.write(b'2')
        elif (len(size) == 3):
            serialComm.write(b'3')
        elif (len(size) == 4):
            serialComm.write(b'4')
        serialComm.write(size)
        while True:
            line = serialComm.readline()
            if (line.__contains__("SUCCESS") or line.__contains__("FAILED")):
                print line
                if(line.__contains__("SUCCESS")):
                    self.emit(SIGNAL('appendST_SIG'), "Success rate of request:  Successful\n")
                    sucAllocs += 1
                    index = line.split(':')[1]
                    addr = line.split(':')[2]
                    duration = line.split(':')[3]
                    duration = duration[:-2]
                    countAllocTime += int(duration)
                    i = 0
                    while True:
                        if (ADDRS[i] == None):
                            break
                        i += 1
                    ADDRS[i] = index
                    self.emit(SIGNAL('appendST_SIG'), "Size of requested block:  " + str(size) + " B\n")
                    size = int(size) + MEM_BLOCK_SIZE
                    self.emit(SIGNAL('appendST_SIG'), "Real size of allocated block: " + str(size) + " B\n")
                    self.emit(SIGNAL('appendST_SIG'), "Request satisfying time: " + str(duration) + " ms\n")
                    self.emit(SIGNAL('appendST_SIG'), "Beggining address of block: " + addr)
                    if (int(duration) <= bestAllocTime):
                        bestAllocTime = int(duration)
                    if (int(duration) >= worstAllocTime):
                        worstAllocTime = int(duration)
                    print "DURATION: %d" % int(duration)
                    if(int(size) < minAllocBlock):
                        minAllocBlock = int(size)
                    if(int(size) > maxAllocBlock):
                        maxAllocBlock = int(size)
                    sizeCount += int(size)
                    averageAllocBlock = (sizeCount / numOfAllocs)
                elif(line.__contains__("FAILED")):
                    self.emit(SIGNAL('appendST_SIG'), "Success rate of request:  Failed\n")
                    remMem = line.split(':')[1]
                    remMem = remMem[:-2]
                    if(int(remMem) > int(size)+MEM_BLOCK_SIZE):
                        self.emit(SIGNAL('appendST_SIG'), "Fail has been caused due to external fragmentation:")
                        self.emit(SIGNAL('appendST_SIG'), "Requested size: " + str(size) + " B\nRemaining memory: "+ str(remMem)+" B")
                        self.emit(SIGNAL('appendST_SIG'), "\nMemory is divided into small blocks\n")
                        numOfExtFragFail += 1

                break
            print line
            time.sleep(0.5)


    def freeMem(self, step):
        global serialComm
        global bestFreeTime, worstFreeTime, sucFrees, countFreeTime
        global stepNum
        numOfJoins = 0
        print "\n -------  Start test FREE  --------- StepNum:"+str(stepNum)
        self.emit(SIGNAL('appendST_SIG'), "Request type:                   Free\n")
        ptr = step.split(' ')[1]
        ptr = ptr[3:]
        ptr = str(ptr)
        if(ADDRS[int(ptr)] == None):
            print "ERROR(Free): index doesnt exists"
            return
        serialComm.write(b'f')
        if (len(ptr) == 1):
            serialComm.write(b'1')
        elif (len(ptr) == 2):
            serialComm.write(b'2')
        elif (len(ptr) == 3):
            serialComm.write(b'3')
        elif (len(ptr) == 4):
            serialComm.write(b'4')
        serialComm.write(ptr)
        while True:
            line = serialComm.readline()
            if (line.__contains__("Free complete")):
                print line
                sucFrees += 1
                duration = line.split(':')[2]
                countFreeTime += int(duration)
                numOfJoins = line.split(':')[3]
                numOfJoins = numOfJoins[:-2]
                self.emit(SIGNAL('appendST_SIG'), "Success rate of request:   Successful\n")
                self.emit(SIGNAL('appendST_SIG'), "Request satisfying time: " + str(duration) + " ms\n")
                self.emit(SIGNAL('appendST_SIG'), "Number of block joins: "+str(numOfJoins)+"\n")
                ADDRS[int(ptr)] = None
                if (int(duration) <= bestFreeTime):
                    bestFreeTime = int(duration)
                if (int(duration) >= worstFreeTime):
                    worstFreeTime = int(duration)
                break
            elif(line.__contains__("FAILED")):
                print "Fail free> "+line
                self.emit(SIGNAL('setST_SIG'), '')
                self.emit(SIGNAL('appendST_SIG'), "Success rate of request:   Failed\n")
                self.emit(SIGNAL('appendST_SIG'), "Request satisfying time: 0ms")
                self.emit(SIGNAL('appendST_SIG'), "Number of block joins: 0")
                break
            print line
            time.sleep(1)

    def reallocMem(self, step):
        global serialComm
        global bestReallocTime, worstReallocTime, sucReallocs, countReallocTime
        global stepNum
        print "\n +++++++++++  Start test realloc +++++++++++ StepNum:"+str(stepNum)
        self.emit(SIGNAL('appendST_SIG'), "Request type:                   Reallocation\n")
        ptr = step.split(' ')[1]
        ptr = ptr[3:]
        ptr = str(ptr)
        size = step.split(' ')[2]
        size = str(size)
        if (ADDRS[int(ptr)] == None):
            print "ERROR(realloc): index doesnt exists"
            return
        serialComm.write(b'r')
        if (len(ptr) == 1):
            serialComm.write(b'1')
        elif (len(ptr) == 2):
            serialComm.write(b'2')
        elif (len(ptr) == 3):
            serialComm.write(b'3')
        elif (len(ptr) == 4):
            serialComm.write(b'4')
        serialComm.write(ptr)

        if (len(size) == 1):
            serialComm.write(b'1')
        elif (len(size) == 2):
            serialComm.write(b'2')
        elif (len(size) == 3):
            serialComm.write(b'3')
        elif (len(size) == 4):
            serialComm.write(b'4')
        serialComm.write(size)
        while True:
            line = serialComm.readline()
            if (line.__contains__("Realloc complete")):
                print line
                sucReallocs += 1
                duration = line.split(':')[1]
                countReallocTime += int(duration)
                addr = line.split(':')[2]
                oldSize = line.split(':')[3]
                oldSize = oldSize[:-2]
                self.emit(SIGNAL('appendST_SIG'), "Success rate of request:   Successful\n")
                self.emit(SIGNAL('appendST_SIG'), "Old size of block:      "+str(oldSize)+"B\n")
                self.emit(SIGNAL('appendST_SIG'), "New size of block:      "+str(size)+"B\n")
                self.emit(SIGNAL('appendST_SIG'), "Request satisfying time: " + str(duration) + " ms\n")
                self.emit(SIGNAL('appendST_SIG'), "Beginning address of new block: "+addr)
                if (int(duration) <= bestReallocTime):
                    bestReallocTime = int(duration)
                if (int(duration) >= worstReallocTime):
                    worstReallocTime = int(duration)
                break
            elif (line.__contains__("FAILED")):
                print line
                self.emit(SIGNAL('setST_SIG'), '')
                self.emit(SIGNAL('appendST_SIG'), "Success rate of request:   Failed\n")
                self.emit(SIGNAL('appendST_SIG'), "Old size of block:      0B")
                self.emit(SIGNAL('appendST_SIG'), "New size of block:      0B")
                self.emit(SIGNAL('appendST_SIG'), "Request satisfying time: 0ms")
                self.emit(SIGNAL('appendST_SIG'), "Beginning address of new block: 0")
                break
            print line
            time.sleep(1)

    def printMem(self):
        global serialComm
        global remainingMem
        global wholeTime
        global numOfFreeBlocks, minFreeBlock, maxFreeBlock, averageFreeBlock
        global numOfUnusable, numOfBlocks
        global minFreeBlock, maxFreeBlock
        print "ACTUAL MEMORY STATE from python PrintMemory"
        self.emit(SIGNAL('setMV_SIG'), '')
        serialComm.write(b'p')
        time.sleep(1)
        numOfFreeBlocks = 0
        numOfBlocks = 0
        numOfUnusable = 0
        minFreeBlock = 5000
        maxFreeBlock = 0

        size = 0
        count = 0
        while True:
            line = serialComm.readline()
            if (line.__contains__("Finish")):
                break
            if (not (line.__contains__("Counter") or line.__contains__("WholeTime"))):
                if (line.__contains__("FREE")):
                    var = line.split(':')[2]
                    var = var[:-6]
                    var = int(var)
                    numOfFreeBlocks += 1
                    if (int(var) < int(minFreeBlock)):
                        minFreeBlock = var
                    if (int(var) > int(maxFreeBlock)):
                        maxFreeBlock = var
                    if (int(var) <= MEM_BLOCK_SIZE):
                        numOfUnusable += 1
                    size += int(var)
                    count += 1
                    averageFreeBlock = (size / count)
                self.emit(SIGNAL('appendMV_SIG'), line)
                numOfBlocks += 1
            if (line.__contains__("Remaining")):
                remainingMem = line.split(':')[1]
                remainingMem = remainingMem[:-2]
                allocatedMem = int(wholeMem) - int(remainingMem)
                percentage = ((float(allocatedMem) / float(wholeMem)) * 100)
                self.emit(SIGNAL('setPB_SIG'), round(float(percentage)))
            if (line.__contains__("WholeTime")):
                var = line.split(':')[1]
                var = var[:-2]
                wholeTime += int(var)
            print line
            time.sleep(0.1)

    def run(self):
        self.nextStep(self.step)



class ExecuteAllStepsThread(QThread):
    def __init__(self, entireTest):
        QThread.__init__(self)
        self.entireTest = entireTest
        self.testing = False

    def __del__(self):
        self.wait()

    def executeAllSteps(self):
        numOfRemainingSteps = self.getNumOfRemainingSteps()
        for x in range(0, numOfRemainingSteps - 1):  # minus 2 because of first and last line in test file
            self.testing = True
            step = self.getStep()
            self.nextStep(step)
            self.testing = False
            time.sleep(2)

    def stopTesting(self):
        while True:
            if self.testing == False:
                self.terminate()
                break
            time.sleep(0.1)

    def getNumOfRemainingSteps(self):
        test = self.entireTest
        steps = test.split('\n')
        return len(steps)

    def getStep(self):
        step = self.entireTest.split('\n')[0]
        stepLength = len(step)
        self.entireTest = self.entireTest[(stepLength+1):]
        self.emit(SIGNAL('setAT_SIG'), self.entireTest)
        return step

    def nextStep(self, step):
        global stepNum, numOfSteps
        stepNum += 1
        p = ((float(stepNum) / float(numOfSteps)) * 100)
        self.emit(SIGNAL('setPBT_SIG'), p)
        self.emit(SIGNAL('appendST_SIG'), 'NEXT STEP')
        self.runStep(step)
        time.sleep(1)
        self.printMem()
        self.emit(SIGNAL('appendES_SIG'), step)
        if (stepNum % 5 == 0):
            self.exportStatsToFile()


    def runStep(self, step):
        global numOfAllocs, numOfFrees, numOfReallocs
        self.emit(SIGNAL('setST_SIG'), '')
        type = step.split(' ')[0]
        if(type == "alloc"):
            numOfAllocs += 1
            self.allocateMem(step)
        if(type == "free"):
            numOfFrees += 1
            self.freeMem(step)
        if(type == "realloc"):
            numOfReallocs += 1
            self.reallocMem(step)


    def allocateMem(self, step):
        global serialComm
        global bestAllocTime, worstAllocTime, sucAllocs, countAllocTime
        global maxAllocBlock, minAllocBlock, averageAllocBlock, sizeCount
        global stepNum, numOfExtFragFail
        print "\n **** Start test allocation **** StepNum:"+str(stepNum)
        self.emit(SIGNAL('appendST_SIG'), "Request type:                   Allocation\n")
        size = step.split(' ')[1]
        size = str(size)
        serialComm.write(b'a')
        if (len(size) == 1):
            serialComm.write(b'1')
        elif (len(size) == 2):
            serialComm.write(b'2')
        elif (len(size) == 3):
            serialComm.write(b'3')
        elif (len(size) == 4):
            serialComm.write(b'4')
        serialComm.write(size)
        while True:
            line = serialComm.readline()
            if (line.__contains__("SUCCESS") or line.__contains__("FAILED")):
                print line
                if(line.__contains__("SUCCESS")):
                    self.emit(SIGNAL('appendST_SIG'), "Success rate of request:  Successful\n")
                    sucAllocs += 1
                    index = line.split(':')[1]
                    addr = line.split(':')[2]
                    duration = line.split(':')[3]
                    duration = duration[:-2]
                    countAllocTime += int(duration)
                    i = 0
                    while True:
                        if (ADDRS[i] == None):
                            break
                        i += 1
                    ADDRS[i] = index
                    self.emit(SIGNAL('appendST_SIG'), "Size of requested block:  " + str(size) + " B\n")
                    size = int(size) + MEM_BLOCK_SIZE
                    self.emit(SIGNAL('appendST_SIG'), "Real size of allocated block: " + str(size) + " B\n")
                    self.emit(SIGNAL('appendST_SIG'), "Request satisfying time: " + str(duration) + " ms\n")
                    self.emit(SIGNAL('appendST_SIG'), "Beggining address of block: " + addr)
                    if (int(duration) <= bestAllocTime):
                        bestAllocTime = int(duration)
                    if (int(duration) >= worstAllocTime):
                        worstAllocTime = int(duration)
                    print "DURATION: %d" % int(duration)
                    if(int(size) < minAllocBlock):
                        minAllocBlock = int(size)
                    if(int(size) > maxAllocBlock):
                        maxAllocBlock = int(size)
                    sizeCount += int(size)
                    averageAllocBlock = (sizeCount / numOfAllocs)
                elif(line.__contains__("FAILED")):
                    self.emit(SIGNAL('appendST_SIG'), "Success rate of request:  Failed\n")
                    remMem = line.split(':')[1]
                    remMem = remMem[:-2]
                    if(int(remMem) > int(size)+MEM_BLOCK_SIZE):
                        self.emit(SIGNAL('appendST_SIG'), "Fail has been caused due to external fragmentation:")
                        self.emit(SIGNAL('appendST_SIG'), "Requested size: " + str(size) + " B\nRemaining memory: "+ str(remMem)+" B")
                        self.emit(SIGNAL('appendST_SIG'), "\nMemory is divided into small blocks\n")
                        numOfExtFragFail += 1

                break
            print line
            time.sleep(0.5)


    def freeMem(self, step):
        global serialComm
        global bestFreeTime, worstFreeTime, sucFrees, countFreeTime
        global stepNum
        numOfJoins = 0
        print "\n -------  Start test FREE  --------- StepNum:"+str(stepNum)
        self.emit(SIGNAL('appendST_SIG'), "Request type:                   Free\n")
        ptr = step.split(' ')[1]
        ptr = ptr[3:]
        ptr = str(ptr)
        if(ADDRS[int(ptr)] == None):
            print "ERROR(Free): index doesnt exists"
            return
        serialComm.write(b'f')
        if (len(ptr) == 1):
            serialComm.write(b'1')
        elif (len(ptr) == 2):
            serialComm.write(b'2')
        elif (len(ptr) == 3):
            serialComm.write(b'3')
        elif (len(ptr) == 4):
            serialComm.write(b'4')
        serialComm.write(ptr)
        while True:
            line = serialComm.readline()
            if (line.__contains__("Free complete")):
                print line
                sucFrees += 1
                duration = line.split(':')[2]
                countFreeTime += int(duration)
                numOfJoins = line.split(':')[3]
                numOfJoins = numOfJoins[:-2]
                self.emit(SIGNAL('appendST_SIG'), "Success rate of request:   Successful\n")
                self.emit(SIGNAL('appendST_SIG'), "Request satisfying time: " + str(duration) + " ms\n")
                self.emit(SIGNAL('appendST_SIG'), "Number of block joins: "+str(numOfJoins)+"\n")
                ADDRS[int(ptr)] = None
                if (int(duration) <= bestFreeTime):
                    bestFreeTime = int(duration)
                if (int(duration) >= worstFreeTime):
                    worstFreeTime = int(duration)
                break
            elif(line.__contains__("FAILED")):
                print "Fail free> "+line
                self.emit(SIGNAL('setST_SIG'), '')
                self.emit(SIGNAL('appendST_SIG'), "Success rate of request:   Failed\n")
                self.emit(SIGNAL('appendST_SIG'), "Request satisfying time: 0ms")
                self.emit(SIGNAL('appendST_SIG'), "Number of block joins: 0")
                break
            print line
            time.sleep(1)

    def reallocMem(self, step):
        global serialComm
        global bestReallocTime, worstReallocTime, sucReallocs, countReallocTime
        global stepNum
        print "\n +++++++++++  Start test realloc +++++++++++ StepNum:"+str(stepNum)
        self.emit(SIGNAL('appendST_SIG'), "Request type:                   Reallocation\n")
        ptr = step.split(' ')[1]
        ptr = ptr[3:]
        ptr = str(ptr)
        size = step.split(' ')[2]
        size = str(size)
        if (ADDRS[int(ptr)] == None):
            print "ERROR(realloc): index doesnt exists"
            return
        serialComm.write(b'r')
        if (len(ptr) == 1):
            serialComm.write(b'1')
        elif (len(ptr) == 2):
            serialComm.write(b'2')
        elif (len(ptr) == 3):
            serialComm.write(b'3')
        elif (len(ptr) == 4):
            serialComm.write(b'4')
        serialComm.write(ptr)

        if (len(size) == 1):
            serialComm.write(b'1')
        elif (len(size) == 2):
            serialComm.write(b'2')
        elif (len(size) == 3):
            serialComm.write(b'3')
        elif (len(size) == 4):
            serialComm.write(b'4')
        serialComm.write(size)
        while True:
            line = serialComm.readline()
            if (line.__contains__("Realloc complete")):
                print line
                sucReallocs += 1
                duration = line.split(':')[1]
                countReallocTime += int(duration)
                addr = line.split(':')[2]
                oldSize = line.split(':')[3]
                oldSize = oldSize[:-2]
                self.emit(SIGNAL('appendST_SIG'), "Success rate of request:   Successful\n")
                self.emit(SIGNAL('appendST_SIG'), "Old size of block:      "+str(oldSize)+"B\n")
                self.emit(SIGNAL('appendST_SIG'), "New size of block:      "+str(size)+"B\n")
                self.emit(SIGNAL('appendST_SIG'), "Request satisfying time: " + str(duration) + " ms\n")
                self.emit(SIGNAL('appendST_SIG'), "Beginning address of new block: "+addr)
                if (int(duration) <= bestReallocTime):
                    bestReallocTime = int(duration)
                if (int(duration) >= worstReallocTime):
                    worstReallocTime = int(duration)
                break
            elif (line.__contains__("FAILED")):
                print line
                self.emit(SIGNAL('setST_SIG'), '')
                self.emit(SIGNAL('appendST_SIG'), "Success rate of request:   Failed\n")
                self.emit(SIGNAL('appendST_SIG'), "Old size of block:      0B")
                self.emit(SIGNAL('appendST_SIG'), "New size of block:      0B")
                self.emit(SIGNAL('appendST_SIG'), "Request satisfying time: 0ms")
                self.emit(SIGNAL('appendST_SIG'), "Beginning address of new block: 0")
                break
            print line
            time.sleep(1)

    def printMem(self):
        global serialComm
        global remainingMem
        global wholeTime
        global numOfFreeBlocks, minFreeBlock, maxFreeBlock, averageFreeBlock
        global numOfUnusable, numOfBlocks
        global minFreeBlock, maxFreeBlock
        print "ACTUAL MEMORY STATE from python PrintMemory"
        self.emit(SIGNAL('setMV_SIG'), '')
        serialComm.write(b'p')
        time.sleep(1)
        numOfFreeBlocks = 0
        numOfBlocks = 0
        numOfUnusable = 0
        minFreeBlock = 5000
        maxFreeBlock = 0

        size = 0
        count = 0
        while True:
            line = serialComm.readline()
            if (line.__contains__("Finish")):
                break
            if (not (line.__contains__("Counter") or line.__contains__("WholeTime"))):
                if (line.__contains__("FREE")):
                    var = line.split(':')[2]
                    var = var[:-6]
                    var = int(var)
                    numOfFreeBlocks += 1
                    if (int(var) < int(minFreeBlock)):
                        minFreeBlock = var
                    if (int(var) > int(maxFreeBlock)):
                        maxFreeBlock = var
                    if (int(var) <= MEM_BLOCK_SIZE):
                        numOfUnusable += 1
                    size += int(var)
                    count += 1
                    averageFreeBlock = (size / count)
                self.emit(SIGNAL('appendMV_SIG'), line)
                numOfBlocks += 1
            if (line.__contains__("Remaining")):
                remainingMem = line.split(':')[1]
                remainingMem = remainingMem[:-2]
                allocatedMem = int(wholeMem) - int(remainingMem)
                percentage = ((float(allocatedMem) / float(wholeMem)) * 100)
                self.emit(SIGNAL('setPB_SIG'), round(float(percentage)))
            if (line.__contains__("WholeTime")):
                var = line.split(':')[1]
                var = var[:-2]
                wholeTime += int(var)
            print line
            time.sleep(0.1)

    def exportStatsToFile(self):
        global numOfAllocs, numOfFrees, numOfReallocs
        global sucAllocs, sucFrees, sucReallocs
        global bestFreeTime, bestReallocTime, bestAllocTime
        global worstFreeTime, worstReallocTime, worstAllocTime
        global countAllocTime, countFreeTime, countReallocTime
        global maxAllocBlock, minAllocBlock, averageAllocBlock
        global numOfFreeBlocks, maxFreeBlock, minFreeBlock, averageFreeBlock, numOfUnusable
        global numOfExtFragFail, numOfBlocks
        try:
            file = open(TEST_DIR+"stats", "w")
            if (int(numOfAllocs) == 0 and int(numOfFrees) == 0 and int(numOfReallocs) == 0):
                file.write("No statistics available\n")
                return
            if (int(numOfAllocs) > 0):
                file.write("Best alloc time: " + str(bestAllocTime) + "ms\n")
                file.write("Worst alloc time: " + str(worstAllocTime) + "ms\n")
                file.write("Jitter: " + str(worstAllocTime - bestAllocTime) + "ms  Average: " + str(
                    countAllocTime / sucAllocs) + "ms\n")
                file.write("\n")
            if (int(numOfFrees) > 0):
                file.write("Best free time: " + str(bestFreeTime) + "ms\n")
                file.write("Worst free time: " + str(worstFreeTime) + "ms\n")
                file.write(
                    "Jitter: " + str(worstFreeTime - bestFreeTime) + "ms  Average: " + str(countFreeTime / sucFrees) + "ms\n")
                file.write("\n")
            if (int(numOfReallocs) > 0):
                file.write("Best realloc time: " + str(bestReallocTime) + "ms\n")
                file.write("Worst realloc time: " + str(worstReallocTime) + "ms\n")
                file.write("Jitter: " + str(worstReallocTime - bestReallocTime) + "ms   Average: " + str(
                    countReallocTime / sucReallocs) + "ms\n")
                file.write("\n")
            file.write("Time count of whole test: " + str(wholeTime) + "ms\n")
            file.write("\n")
            file.write("External fragmentation:\n")
            file.write("Largest free blok: " + str(maxFreeBlock) + "B\n")
            file.write("Smallet free block: " + str(minFreeBlock) + "B\n")
            file.write("Average free block: " + str(averageFreeBlock) + "B\n")
            file.write("Number of free blocks: " + str(numOfFreeBlocks)+"\n")
            file.write("Number of unusable blocks: " + str(numOfUnusable)+"\n")
            file.write("\n")
            intFrag = round((float((numOfBlocks - 2) * MEM_BLOCK_SIZE) / float(wholeMem-int(remainingMem))) * 100)
            file.write("Internal fragmentation: " + str((numOfBlocks - 2) * MEM_BLOCK_SIZE) + "B (" + str(intFrag) + "%)\n")
            file.write("\n")
            file.write("Type and number of requests: \n")
            file.write("(all / success / failed / percentage of success)\n")
            if (int(numOfAllocs) > 0):
                allocPercentage = str(round((float(sucAllocs) / float(numOfAllocs)) * 100, 3))
                file.write("Allocs: " + str(numOfAllocs) + " / " + str(sucAllocs) + " / " + str(
                    int(numOfAllocs) - int(sucAllocs)) + " / " + allocPercentage + "%\n")
            if (int(numOfFrees) > 0):
                freePercentage = str(round((float(sucFrees) / float(numOfFrees)) * 100, 3))
                file.write("Frees: " + str(numOfFrees) + " / " + str(sucFrees) + " / " + str(
                    int(numOfFrees) - int(sucFrees)) + " / " + freePercentage + "%\n")
            if (int(numOfReallocs) > 0):
                reallocPercentage = str(round((float(sucReallocs) / float(numOfReallocs)) * 100, 3))
                file.write("Reallocs: " + str(numOfReallocs) + " / " + str(sucReallocs) + " / " + str(
                    int(numOfReallocs) - int(sucReallocs)) + " /" + reallocPercentage + "%\n")
            file.write("\n")
            file.write("Memory utilization:\n")
            file.write("Whole memory:  " + str(wholeMem) + "B\n")
            allocMemPercentage = str(round(((float(int(wholeMem) - int(remainingMem)) / float(wholeMem)) * 100), 3))
            file.write(
                "Allocated memory:  " + str(int(wholeMem) - int(remainingMem)) + "B  (" + str(allocMemPercentage) + " %)\n")
            freeMemPercentage = str(round(((float(remainingMem) / float(wholeMem)) * 100), 3))
            file.write("Free memory:  " + str(remainingMem) + "B  (" + str(freeMemPercentage) + " %)\n")
            file.write("\n")
            # ui.appendST("Largest allocated block: "+str(maxAllocBlock)+"B")
            # ui.appendST("Smallest allocated block: "+str(minAllocBlock)+"B")
            # ui.appendST("Average allocatd block: " + str(averageAllocBlock) + "B")
            file.write("Number of allocation fails due to external fagmentation: " + str(numOfExtFragFail)+"\n")
            file.close()
        except Exception:
                print "File not found"
                return


    def run(self):
        self.executeAllSteps()


# ************************************************
#
#             PRINT FUNCTIONS
#
#*************************************************

class PrintMemoryThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()


    def printMemory(self):
        global serialComm
        global remainingMem
        global wholeTime
        global numOfFreeBlocks, minFreeBlock, maxFreeBlock, averageFreeBlock
        global numOfUnusable, numOfBlocks
        global minFreeBlock, maxFreeBlock
        print "ACTUAL MEMORY STATE from python PrintMemory"
        self.emit(SIGNAL('setMV_SIG'), '')
        serialComm.write(b'p')
        time.sleep(1)
        numOfFreeBlocks = 0
        numOfBlocks = 0
        numOfUnusable = 0
        minFreeBlock = 5000
        maxFreeBlock = 0

        size = 0
        count = 0
        while True:
            line = serialComm.readline()
            if (line.__contains__("Finish")):
                break
            if(not (line.__contains__("Counter") or line.__contains__("WholeTime"))):
                if(line.__contains__("FREE")):
                    var = line.split(':')[2]
                    var = var[:-6]
                    var = int(var)
                    numOfFreeBlocks += 1
                    if(int(var) < int(minFreeBlock)):
                        minFreeBlock = var
                    if(int(var) > int(maxFreeBlock)):
                        maxFreeBlock = var
                    if(int(var) <= MEM_BLOCK_SIZE):
                        numOfUnusable += 1
                    size += int(var)
                    count += 1
                    averageFreeBlock = (size / count)
                self.emit(SIGNAL('appendMV_SIG'), line)
                numOfBlocks += 1
            if(line.__contains__("Remaining")):
                remainingMem = line.split(':')[1]
                remainingMem = remainingMem[:-2]
                allocatedMem = int(wholeMem) - int(remainingMem)
                percentage = ((float(allocatedMem) / float(wholeMem)) * 100)
                self.emit(SIGNAL('setPB_SIG'), round(float(percentage)))
            if(line.__contains__("WholeTime")):
                var = line.split(':')[1]
                var = var[:-2]
                wholeTime += int(var)
            print line
            time.sleep(0.1)

    def run(self):
        self.printMemory()



class ShowAllStatsThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def showAllStats(self):
        global numOfAllocs, numOfFrees, numOfReallocs
        global sucAllocs, sucFrees, sucReallocs
        global bestFreeTime, bestReallocTime, bestAllocTime
        global worstFreeTime, worstReallocTime, worstAllocTime
        global countAllocTime, countFreeTime, countReallocTime
        global maxAllocBlock, minAllocBlock, averageAllocBlock
        global numOfFreeBlocks, maxFreeBlock, minFreeBlock, averageFreeBlock, numOfUnusable
        global numOfExtFragFail, numOfBlocks
        self.emit(SIGNAL('setST_SIG'), '')
        if(int(numOfAllocs) == 0 and int(numOfFrees) == 0 and int(numOfReallocs) == 0):
            self.emit(SIGNAL('appendST_SIG'), 'No statistics available')
            return
        if(int(numOfAllocs) > 0):
            self.emit(SIGNAL('appendST_SIG'), "Best alloc time: "+str(bestAllocTime)+"ms")
            self.emit(SIGNAL('appendST_SIG'), "Worst alloc time: "+str(worstAllocTime)+"ms")
            self.emit(SIGNAL('appendST_SIG'), "Jitter: " + str(worstAllocTime - bestAllocTime) +"ms  Average: " + str(countAllocTime / sucAllocs) + "ms")
            self.emit(SIGNAL('appendST_SIG'), '')
        if(int(numOfFrees) > 0):
            self.emit(SIGNAL('appendST_SIG'), "Best free time: " + str(bestFreeTime)+"ms")
            self.emit(SIGNAL('appendST_SIG'), "Worst free time: " + str(worstFreeTime)+"ms")
            self.emit(SIGNAL('appendST_SIG'), "Jitter: " + str(worstFreeTime - bestFreeTime) +"ms  Average: " + str(countFreeTime / sucFrees) + "ms")
            self.emit(SIGNAL('appendST_SIG'), '')
        if(int(numOfReallocs) > 0):
            self.emit(SIGNAL('appendST_SIG'), "Best realloc time: " + str(bestReallocTime)+"ms")
            self.emit(SIGNAL('appendST_SIG'), "Worst realloc time: " + str(worstReallocTime)+"ms")
            self.emit(SIGNAL('appendST_SIG'), "Jitter: " + str(worstReallocTime - bestReallocTime) +"ms   Average: " + str(countReallocTime / sucReallocs) + "ms")
            self.emit(SIGNAL('appendST_SIG'), '')
        self.emit(SIGNAL('appendST_SIG'), "Time count of whole test: "+str(wholeTime)+"ms")
        self.emit(SIGNAL('appendST_SIG'), '')
        self.emit(SIGNAL('appendST_SIG'), 'External fragmentation:')
        self.emit(SIGNAL('appendST_SIG'), "Largest free blok: "+str(maxFreeBlock)+"B")
        self.emit(SIGNAL('appendST_SIG'), "Smallet free block: "+str(minFreeBlock)+"B")
        self.emit(SIGNAL('appendST_SIG'), "Average free block: "+str(averageFreeBlock)+"B")
        self.emit(SIGNAL('appendST_SIG'), "Number of free blocks: "+str(numOfFreeBlocks))
        self.emit(SIGNAL('appendST_SIG'), "Number of unusable blocks: "+str(numOfUnusable))
        self.emit(SIGNAL('appendST_SIG'), '')
        intFrag = round((float((numOfBlocks-2)*MEM_BLOCK_SIZE) / float(wholeMem-int(remainingMem))) * 100)
        self.emit(SIGNAL('appendST_SIG'), "Internal fragmentation: "+str((numOfBlocks-2)*MEM_BLOCK_SIZE)+"B ("+str(intFrag)+"%)")
        self.emit(SIGNAL('appendST_SIG'), '')
        self.emit(SIGNAL('appendST_SIG'), 'Type and number of requests: ')
        self.emit(SIGNAL('appendST_SIG'), '(all / success / failed / percentage of success)')
        if(int(numOfAllocs) > 0):
            allocPercentage = str(round((float(sucAllocs) / float(numOfAllocs)) * 100,3))
            self.emit(SIGNAL('appendST_SIG'), "Allocs: "+str(numOfAllocs)+" / "+str(sucAllocs)+" / "+str(int(numOfAllocs) - int(sucAllocs))+" / "+allocPercentage+"%")
        if(int(numOfFrees) > 0):
            freePercentage = str(round((float(sucFrees) / float(numOfFrees)) * 100,3))
            self.emit(SIGNAL('appendST_SIG'), "Frees: "+str(numOfFrees)+" / "+str(sucFrees)+" / "+str(int(numOfFrees) - int(sucFrees))+" / "+freePercentage+"%")
        if (int(numOfReallocs) > 0):
            reallocPercentage = str(round((float(sucReallocs) / float(numOfReallocs)) * 100,3))
            self.emit(SIGNAL('appendST_SIG'), "Reallocs: "+str(numOfReallocs)+" / "+str(sucReallocs)+" / "+str(int(numOfReallocs) - int(sucReallocs))+" /"+reallocPercentage+"%")
        self.emit(SIGNAL('appendST_SIG'), '')
        self.emit(SIGNAL('appendST_SIG'), 'Memory utilization:')
        self.emit(SIGNAL('appendST_SIG'), "Whole memory:  "+str(wholeMem)+"B")
        allocMemPercentage = str(round(((float(int(wholeMem) - int(remainingMem)) / float(wholeMem)) * 100),3))
        self.emit(SIGNAL('appendST_SIG'), "Allocated memory:  "+str(int(wholeMem) - int(remainingMem))+"B  ("+str(allocMemPercentage)+" %)")
        freeMemPercentage = str(round(((float(remainingMem) / float(wholeMem)) * 100),3))
        self.emit(SIGNAL('appendST_SIG'), "Free memory:  "+str(remainingMem)+"B  ("+str(freeMemPercentage)+" %)")
        self.emit(SIGNAL('appendST_SIG'), '')
        self.emit(SIGNAL('appendST_SIG'), "Number of allocation fails due to external fagmentation: "+str(numOfExtFragFail))
        self.emit(SIGNAL('setPB_SIG'), allocMemPercentage)
        self.exportStatsToFile()


    def exportStatsToFile(self):
        global numOfAllocs, numOfFrees, numOfReallocs
        global sucAllocs, sucFrees, sucReallocs
        global bestFreeTime, bestReallocTime, bestAllocTime
        global worstFreeTime, worstReallocTime, worstAllocTime
        global countAllocTime, countFreeTime, countReallocTime
        global maxAllocBlock, minAllocBlock, averageAllocBlock
        global numOfFreeBlocks, maxFreeBlock, minFreeBlock, averageFreeBlock, numOfUnusable
        global numOfExtFragFail, numOfBlocks
        try:
            file = open(TEST_DIR+"stats", "w")
            if (int(numOfAllocs) == 0 and int(numOfFrees) == 0 and int(numOfReallocs) == 0):
                file.write("No statistics available\n")
                return
            if (int(numOfAllocs) > 0):
                file.write("Best alloc time: " + str(bestAllocTime) + "ms\n")
                file.write("Worst alloc time: " + str(worstAllocTime) + "ms\n")
                file.write("Jitter: " + str(worstAllocTime - bestAllocTime) + "ms  Average: " + str(
                    countAllocTime / sucAllocs) + "ms\n")
                file.write("\n")
            if (int(numOfFrees) > 0):
                file.write("Best free time: " + str(bestFreeTime) + "ms\n")
                file.write("Worst free time: " + str(worstFreeTime) + "ms\n")
                file.write(
                    "Jitter: " + str(worstFreeTime - bestFreeTime) + "ms  Average: " + str(countFreeTime / sucFrees) + "ms\n")
                file.write("\n")
            if (int(numOfReallocs) > 0):
                file.write("Best realloc time: " + str(bestReallocTime) + "ms\n")
                file.write("Worst realloc time: " + str(worstReallocTime) + "ms\n")
                file.write("Jitter: " + str(worstReallocTime - bestReallocTime) + "ms   Average: " + str(
                    countReallocTime / sucReallocs) + "ms\n")
                file.write("\n")
            file.write("Time count of whole test: " + str(wholeTime) + "ms\n")
            file.write("\n")
            file.write("External fragmentation:\n")
            file.write("Largest free blok: " + str(maxFreeBlock) + "B\n")
            file.write("Smallet free block: " + str(minFreeBlock) + "B\n")
            file.write("Average free block: " + str(averageFreeBlock) + "B\n")
            file.write("Number of free blocks: " + str(numOfFreeBlocks)+"\n")
            file.write("Number of unusable blocks: " + str(numOfUnusable)+"\n")
            file.write("\n")
            intFrag = round((float((numOfBlocks - 2) * MEM_BLOCK_SIZE) / float(wholeMem-int(remainingMem))) * 100)
            file.write("Internal fragmentation: " + str((numOfBlocks - 2) * MEM_BLOCK_SIZE) + "B (" + str(intFrag) + "%)\n")
            file.write("\n")
            file.write("Type and number of requests: \n")
            file.write("(all / success / failed / percentage of success)\n")
            if (int(numOfAllocs) > 0):
                allocPercentage = str(round((float(sucAllocs) / float(numOfAllocs)) * 100, 3))
                file.write("Allocs: " + str(numOfAllocs) + " / " + str(sucAllocs) + " / " + str(
                    int(numOfAllocs) - int(sucAllocs)) + " / " + allocPercentage + "%\n")
            if (int(numOfFrees) > 0):
                freePercentage = str(round((float(sucFrees) / float(numOfFrees)) * 100, 3))
                file.write("Frees: " + str(numOfFrees) + " / " + str(sucFrees) + " / " + str(
                    int(numOfFrees) - int(sucFrees)) + " / " + freePercentage + "%\n")
            if (int(numOfReallocs) > 0):
                reallocPercentage = str(round((float(sucReallocs) / float(numOfReallocs)) * 100, 3))
                file.write("Reallocs: " + str(numOfReallocs) + " / " + str(sucReallocs) + " / " + str(
                    int(numOfReallocs) - int(sucReallocs)) + " /" + reallocPercentage + "%\n")
            file.write("\n")
            file.write("Memory utilization:\n")
            file.write("Whole memory:  " + str(wholeMem) + "B\n")
            allocMemPercentage = str(round(((float(int(wholeMem) - int(remainingMem)) / float(wholeMem)) * 100), 3))
            file.write(
                "Allocated memory:  " + str(int(wholeMem) - int(remainingMem)) + "B  (" + str(allocMemPercentage) + " %)\n")
            freeMemPercentage = str(round(((float(remainingMem) / float(wholeMem)) * 100), 3))
            file.write("Free memory:  " + str(remainingMem) + "B  (" + str(freeMemPercentage) + " %)\n")
            file.write("\n")
            # ui.appendST("Largest allocated block: "+str(maxAllocBlock)+"B")
            # ui.appendST("Smallest allocated block: "+str(minAllocBlock)+"B")
            # ui.appendST("Average allocatd block: " + str(averageAllocBlock) + "B")
            file.write("Number of allocation fails due to external fagmentation: " + str(numOfExtFragFail)+"\n")
            file.close()
        except Exception:
                print "File not found"
                return

    def run(self):
        self.showAllStats()