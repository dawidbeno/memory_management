import serial
import time


TEST_DIR = "/home/dejvid/tests/"
serialComm = None

BEST = 'b'
WORST = 'w'

ALGORITHM = BEST
ADDRS = [None]


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
    return "SUCCESS"





# *********************************************
#
#              EXECUTE FUNCTIONS
#
# *********************************************

def runStep(ui, step):
    global serialComm
    print "Start test allocation"
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
            ui.setST("ALOCATION SUCCESS from runStep")
            break
        print line
        time.sleep(0.1)






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

