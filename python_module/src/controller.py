import serial
import time


TEST_DIR = "/home/dejvid/tests/"
serialComm = None

BEST = 'b'
WORST = 'w'

ALGORITHM = BEST
ADDRS = [None]

MEM_BLOCK_SIZE = 6


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
    ui.setST("")
    type = step.split(' ')[0]
    if(type == "alloc"):
        allocateMem(ui, step)
    if(type == "free"):
        ui.appendST("Request type:                   Free\n")
        freeMem(ui, step)
    if(type == "realloc"):
        ui.appendST("Request type:                   Reallocation\n")
        reallocMem(ui, step)


def allocateMem(ui, step):
    global serialComm
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
    ui.appendST("Size of requested block:  "+size+" B\n")
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
            ui.appendST("Request satisfying time: "+str(duration)+" ms\n")
            size = int(size)+MEM_BLOCK_SIZE
            ui.appendST("Real size of allocated block: "+str(size)+" B\n")
            ui.appendST("Beggining address of block: "+addr)
            break
        print line
        time.sleep(0.1)


def freeMem(ui, step):
    global serialComm
    print "Start test free"
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
            ui.appendST("FREE COMPLETE from freeMem")
            ADDRS[int(ptr)] = None
            break
        print line
        time.sleep(1)


def reallocMem(ui, step):
    global serialComm
    print "Start test realloc"
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
            ui.appendST("Realloc success")
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

