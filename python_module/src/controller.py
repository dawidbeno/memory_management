import serial
import time


TEST_DIR = "/home/dejvid/tests/"
serialComm = None

BEST = 'b'
WORST = 'w'

ALGORITHM = BEST
ADDRS = [None]

MEM_BLOCK_SIZE = 6


numOfAllocs = 0
numOfFrees = 0
numOfReallocs = 0

bestAllocTime = 9999
worstAllocTime = 0

bestFreeTime = 9999
worstFreeTime = 0

bestReallocTime = 9999
worstReallocTime = 0


# Arduino uses BEST fit as default algorithm


# *****************************************
#
#            INIT FUNCTION
#
# *****************************************


def init(ui):
    global serialComm
    try:
        serialComm = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(1)
        var = serialComm.readline()
        serialComm.write(b'i')
        while 1:
            time.sleep(1)
            var = serialComm.readline()
            if (var == "INIT\r\n"):
                print "init successful"
                ui.appendST("Init successful")
                setAlgorithm(ui, BEST)
                printMemory(ui)
                break
            else:
                print "waiting for init ..."
    except Exception:
        print "Serial port not found"



def setAlgorithm(ui, algType):
    global serialComm, BEST, WORST, ALGORITHM
    global numOfAllocs, numOfFrees, numOfReallocs
    global bestFreeTime, bestReallocTime, bestAllocTime
    global worstFreeTime, worstReallocTime, worstAllocTime
    numOfAllocs = 0
    numOfFrees = 0
    numOfReallocs = 0
    bestAllocTime = 9999999
    worstAllocTime = 0
    bestFreeTime = 999999
    worstFreeTime = 0
    bestReallocTime = 999999
    worstReallocTime = 0
    ui.setST("")
    if(algType == BEST):
        serialComm.write(b'b')
        while True:
            var = serialComm.readline()
            if(var.__contains__("Alg changed to:")):
                var2 = var.split(':')[1]
                var = var2[0]
                if(var == 'b'):
                    ALGORITHM = "BEST"
                    print "Set alg to BEST"
                    ui.appendST("Algorithm is set to BEST")
                    ui.setAlg(BEST)
                    printMemory(ui)
                    break
            print "waiting to set algorithm ..."
            time.sleep(0.1)

    elif(algType == WORST):
        serialComm.write(b'w')
        while True:
            var = serialComm.readline()
            if (var.__contains__("Alg changed to:")):
                var2 = var.split(':')[1]
                var = var2[0]
                if(var == 'w'):
                    ALGORITHM = "WORST"
                    print "Set alg to WORST"
                    ui.appendST("Algorithm is set to WORST")
                    ui.setAlg(WORST)
                    printMemory(ui)
                    break
            print "waiting to set algorithm ..."
            time.sleep(0.1)

    else:
        print "Bad type of algorithm"
        print "Type \"help\" for more info"





# ***************************************
#
#            LOAD FUNCTIONS
#
# ***************************************

def load_1(ui):
    global TEST_DIR, ADDRS
    try:
        file = open(TEST_DIR+"level_1", "r").read()
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

def load_2(ui):
    global TEST_DIR, ADDRS
    try:
        file = open(TEST_DIR+"level_2", "r").read()
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

def load_3(ui):
    global TEST_DIR, ADDRS
    try:
        file = open(TEST_DIR+"level_3", "r").read()
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

def load_4(ui):
    global TEST_DIR, ADDRS
    try:
        file = open(TEST_DIR+"level_4", "r").read()
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


def nextStep(ui, step):
    ui.appendST("NEXT STEP")
    runStep(ui, step)
    time.sleep(2)
    printMemory(ui)





# *********************************************
#
#              EXECUTE FUNCTIONS
#
# *********************************************

def runStep(ui, step):
    global numOfAllocs, numOfFrees, numOfReallocs
    ui.setST("")
    type = step.split(' ')[0]
    if(type == "alloc"):
        numOfAllocs += 1
        allocateMem(ui, step)
    if(type == "free"):
        numOfFrees += 1
        freeMem(ui, step)
    if(type == "realloc"):
        numOfReallocs += 1
        reallocMem(ui, step)


def allocateMem(ui, step):
    global serialComm
    global bestAllocTime, worstAllocTime
    print "Start test allocation"
    ui.appendST("Request type:                   Allocation\n")
    size = step.split(' ')[1]
    size = str(size)
    serialComm.write(b'a')
    # serial.write(len(size)) NEFUNGUJE a neviem preco :(
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
            index = line.split(':')[1]
            addr = line.split(':')[2]
            duration = line.split(':')[3]
            duration = duration[:-2]
            i = 0
            while True:
                if (ADDRS[i] == None):
                    break
                i += 1
            ADDRS[i] = index
            if(line.__contains__("SUCCESS")):
                ui.appendST("Success rate of request:  Successful\n")
            elif(line.__contains__("FAILED")):
                ui.appendST("Success rate of request:  Failed\n")
            ui.appendST("Size of requested block:  " + str(size) + " B\n")
            size = int(size) + MEM_BLOCK_SIZE
            ui.appendST("Real size of allocated block: "+str(size)+" B\n")
            ui.appendST("Request satisfying time: " + str(duration) + " ms\n")
            ui.appendST("Beggining address of block: "+addr)
            if(int(duration) <= bestAllocTime):
                bestAllocTime = duration
            if(int(duration) >= worstAllocTime):
                worstAllocTime = duration
            break
        print line
        time.sleep(0.1)


def freeMem(ui, step):
    global serialComm
    global bestFreeTime, worstFreeTime
    print "Start test free"
    ui.appendST("Request type:                   Free\n")
    ptr = step.split(' ')[1]
    ptr = ptr[3:]
    ptr = str(ptr)
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
            duration = line.split(':')[2]
            duration = duration[:-2]
            ui.appendST("Success rate of request:   Successful\n")
            ui.appendST("Request satisfying time: " + str(duration) + " ms\n")
            ADDRS[int(ptr)] = None
            if (int(duration) <= bestFreeTime):
                bestFreeTime = duration
            if (int(duration) >= worstFreeTime):
                worstFreeTime = duration
            break
        print line
        time.sleep(1)


def reallocMem(ui, step):
    global serialComm
    global bestReallocTime, worstReallocTime
    print "Start test realloc"
    ui.appendST("Request type:                   Reallocation\n")
    ptr = step.split(' ')[1]
    ptr = ptr[3:]
    ptr = str(ptr)
    size = step.split(' ')[2]
    size = str(size)

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
            duration = line.split(':')[1]
            addr = line.split(':')[2]
            oldSize = line.split(':')[3]
            oldSize = oldSize[:-2]
            ui.appendST("Success rate of request:   Successful\n")
            ui.appendST("Old size of block:      "+str(oldSize)+"B\n")
            ui.appendST("New size of block:      "+str(size)+"B\n")
            ui.appendST("Request satisfying time: " + str(duration) + " ms\n")
            ui.appendST("Beginning address of new block: "+addr)
            if (int(duration) <= bestReallocTime):
                bestReallocTime = duration
            if (int(duration) >= worstReallocTime):
                worstReallocTime = duration
            break
        print line
        time.sleep(1)


# ************************************************
#
#             PRINT FUNCTIONS
#
#*************************************************

def printMemory(ui):
    global serialComm
    print "ACTUAL MEMORY STATE from python PrintMemory"
    ui.setMV("")
    serialComm.write(b'p')
    while True:
        line = serialComm.readline()
        if (line.__contains__("Finish")):
            break
        if(not line.__contains__("Counter")):
            ui.appendMV(line)
        print line
        time.sleep(0.1)


def showAllStats(ui):
    global numOfAllocs, numOfFrees, numOfReallocs
    global bestFreeTime, bestReallocTime, bestAllocTime
    global worstFreeTime, worstReallocTime, worstAllocTime
    ui.setST("")
    ui.appendST("Best alloc time: "+str(bestAllocTime)+"ms")
    ui.appendST("Worst alloc time: "+str(worstAllocTime)+"ms")
    ui.appendST("")
    ui.appendST("Best free time: " + str(bestFreeTime)+"ms")
    ui.appendST("Worst free time: " + str(worstFreeTime)+"ms")
    ui.appendST("")
    ui.appendST("Best realloc time: " + str(bestReallocTime)+"ms")
    ui.appendST("Worst realloc time: " + str(worstReallocTime)+"ms")
    ui.appendST("")





# ****** private functions ******

def sendPtrNum(ui, ptrNum):
    global serialComm
    serialComm.write(b'n')
    if (len(ptrNum) == 1):
        serialComm.write(b'1')
    elif (len(ptrNum) == 2):
        serialComm.write(b'2')
    elif (len(ptrNum) == 3):
        serialComm.write(b'3')
    elif (len(ptrNum) == 4):
        serialComm.write(b'4')
    serialComm.write(ptrNum)
    while True:
        line = serialComm.readline()
        if(line.__contains__("Test prepare finish")):
            print line
            ui.appendST("Test prepare finish")
            break
        print line
        time.sleep(0.1)

