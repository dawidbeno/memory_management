import serial
import time


TEST_DIR = "/home/dejvid/tests/"
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
                break
            else:
                print "waiting for init ..."
    except Exception:
        print "Serial port not found"
        ui.appnedST("FATAL ERROR: Serial port not found. Communication will not work")



def setAlgorithm(ui, algType):
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
    countAllocTime =0
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
    ui.setST("")
    ui.setAT("")
    ui.setES("")
    ui.setPBT(0)
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
    global TEST_DIR, ADDRS, stepNum, numOfSteps
    stepNum = 0
    try:
        file = open(TEST_DIR+"level_1", "r").read()
        numOfSteps = sum(1 for line in open(TEST_DIR+"level_1"))
        numOfSteps -= 2
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
    global TEST_DIR, ADDRS, stepNum, numOfSteps
    stepNum = 0
    try:
        file = open(TEST_DIR+"level_2", "r").read()
        numOfSteps = sum(1 for line in open(TEST_DIR + "level_2"))
        numOfSteps -= 2
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
    global TEST_DIR, ADDRS, stepNum, numOfSteps
    stepNum = 0
    try:
        file = open(TEST_DIR+"level_3", "r").read()
        numOfSteps = sum(1 for line in open(TEST_DIR + "level_3"))
        numOfSteps -= 2
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
    global TEST_DIR, ADDRS, stepNum, numOfSteps
    stepNum = 0
    try:
        file = open(TEST_DIR+"level_4", "r").read()
        numOfSteps = sum(1 for line in open(TEST_DIR + "level_4"))
        numOfSteps -= 2
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
    global stepNum, numOfSteps
    stepNum += 1
    p = ((float(stepNum) / float(numOfSteps)) *100)
    ui.setPBT(p)
    ui.appendST("NEXT STEP")
    runStep(ui, step)
    time.sleep(1)
    printMemory(ui)
    ui.appendES(step)
    if(stepNum % 5 == 0):
        exportStatsToFile()



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
    global bestAllocTime, worstAllocTime, sucAllocs, countAllocTime
    global maxAllocBlock, minAllocBlock, averageAllocBlock, sizeCount
    global stepNum, numOfExtFragFail
    print "\n **** Start test allocation **** StepNum:"+str(stepNum)
    ui.appendST("Request type:                   Allocation\n")
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
                ui.appendST("Success rate of request:  Successful\n")
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
                ui.appendST("Size of requested block:  " + str(size) + " B\n")
                size = int(size) + MEM_BLOCK_SIZE
                ui.appendST("Real size of allocated block: " + str(size) + " B\n")
                ui.appendST("Request satisfying time: " + str(duration) + " ms\n")
                ui.appendST("Beggining address of block: " + addr)
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
                ui.appendST("Success rate of request:  Failed\n")
                remMem = line.split(':')[1]
                remMem = remMem[:-2]
                if(int(remMem) > int(size)+MEM_BLOCK_SIZE):
                    ui.appendST("Fail has been caused due to external fragmentation:")
                    ui.appendST("Requested size: " + str(size) + " B\nRemaining memory: "+ str(remMem)+" B")
                    ui.appendST("\nMemory is divided into small blocks\n")
                    numOfExtFragFail += 1

            break
        print line
        time.sleep(0.5)


def freeMem(ui, step):
    global serialComm
    global bestFreeTime, worstFreeTime, sucFrees, countFreeTime
    global stepNum
    numOfJoins = 0
    print "\n -------  Start test FREE  --------- StepNum:"+str(stepNum)
    ui.appendST("Request type:                   Free\n")
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
            ui.appendST("Success rate of request:   Successful\n")
            ui.appendST("Request satisfying time: " + str(duration) + " ms\n")
            ui.appendST("Number of block joins: "+str(numOfJoins)+"\n")
            ADDRS[int(ptr)] = None
            if (int(duration) <= bestFreeTime):
                bestFreeTime = int(duration)
            if (int(duration) >= worstFreeTime):
                worstFreeTime = int(duration)
            break
        elif(line.__contains__("FAILED")):
            print "Fail free> "+line
            ui.setST("")
            ui.appendST("Success rate of request:   Failed\n")
            ui.appendST("Request satisfying time: 0ms")
            ui.appendST("Number of block joins: 0")
            break
        print line
        time.sleep(1)


def reallocMem(ui, step):
    global serialComm
    global bestReallocTime, worstReallocTime, sucReallocs, countReallocTime
    global stepNum
    print "\n +++++++++++  Start test realloc +++++++++++ StepNum:"+str(stepNum)
    ui.appendST("Request type:                   Reallocation\n")
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
            ui.appendST("Success rate of request:   Successful\n")
            ui.appendST("Old size of block:      "+str(oldSize)+"B\n")
            ui.appendST("New size of block:      "+str(size)+"B\n")
            ui.appendST("Request satisfying time: " + str(duration) + " ms\n")
            ui.appendST("Beginning address of new block: "+addr)
            if (int(duration) <= bestReallocTime):
                bestReallocTime = int(duration)
            if (int(duration) >= worstReallocTime):
                worstReallocTime = int(duration)
            break
        elif (line.__contains__("FAILED")):
            print line
            ui.setST("")
            ui.appendST("Success rate of request:   Failed\n")
            ui.appendST("Old size of block:      0B")
            ui.appendST("New size of block:      0B")
            ui.appendST("Request satisfying time: 0ms")
            ui.appendST("Beginning address of new block: 0")
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
    global remainingMem
    global wholeTime
    global numOfFreeBlocks, minFreeBlock, maxFreeBlock, averageFreeBlock
    global numOfUnusable, numOfBlocks
    global minFreeBlock, maxFreeBlock
    print "ACTUAL MEMORY STATE from python PrintMemory"
    ui.setMV("")
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
            ui.appendMV(line)
            numOfBlocks += 1
        if(line.__contains__("Remaining")):
            remainingMem = line.split(':')[1]
            remainingMem = remainingMem[:-2]
            allocatedMem = int(wholeMem) - int(remainingMem)
            percentage = ((float(allocatedMem) / float(wholeMem)) * 100)
            ui.setPB(round(float(percentage)))
        if(line.__contains__("WholeTime")):
            var = line.split(':')[1]
            var = var[:-2]
            wholeTime += int(var)
        print line
        time.sleep(0.1)


def showAllStats(ui):
    global numOfAllocs, numOfFrees, numOfReallocs
    global sucAllocs, sucFrees, sucReallocs
    global bestFreeTime, bestReallocTime, bestAllocTime
    global worstFreeTime, worstReallocTime, worstAllocTime
    global countAllocTime, countFreeTime, countReallocTime
    global maxAllocBlock, minAllocBlock, averageAllocBlock
    global numOfFreeBlocks, maxFreeBlock, minFreeBlock, averageFreeBlock, numOfUnusable
    global numOfExtFragFail, numOfBlocks
    ui.setST("")
    if(int(numOfAllocs) == 0 and int(numOfFrees) == 0 and int(numOfReallocs) == 0):
        ui.appendST("No statistics available")
        return
    if(int(numOfAllocs) > 0):
        ui.appendST("Best alloc time: "+str(bestAllocTime)+"ms")
        ui.appendST("Worst alloc time: "+str(worstAllocTime)+"ms")
        ui.appendST("Jitter: " + str(worstAllocTime - bestAllocTime) +"ms  Average: " + str(countAllocTime / sucAllocs) + "ms")
        ui.appendST("")
    if(int(numOfFrees) > 0):
        ui.appendST("Best free time: " + str(bestFreeTime)+"ms")
        ui.appendST("Worst free time: " + str(worstFreeTime)+"ms")
        ui.appendST("Jitter: " + str(worstFreeTime - bestFreeTime) +"ms  Average: " + str(countFreeTime / sucFrees) + "ms")
        ui.appendST("")
    if(int(numOfReallocs) > 0):
        ui.appendST("Best realloc time: " + str(bestReallocTime)+"ms")
        ui.appendST("Worst realloc time: " + str(worstReallocTime)+"ms")
        ui.appendST("Jitter: " + str(worstReallocTime - bestReallocTime) +"ms   Average: " + str(countReallocTime / sucReallocs) + "ms")
        ui.appendST("")
    ui.appendST("Time count of whole test: "+str(wholeTime)+"ms")
    ui.appendST("")
    ui.appendST("External fragmentation:")
    ui.appendST("Largest free blok: "+str(maxFreeBlock)+"B")
    ui.appendST("Smallet free block: "+str(minFreeBlock)+"B")
    ui.appendST("Average free block: "+str(averageFreeBlock)+"B")
    ui.appendST("Number of free blocks: "+str(numOfFreeBlocks))
    ui.appendST("Number of unusable blocks: "+str(numOfUnusable))
    ui.appendST("")
    intFrag = round((float((numOfBlocks-2)*MEM_BLOCK_SIZE) / float(wholeMem-int(remainingMem))) * 100)
    ui.appendST("Internal fragmentation: "+str((numOfBlocks-2)*MEM_BLOCK_SIZE)+"B ("+str(intFrag)+"%)")
    ui.appendST("")
    ui.appendST("Type and number of requests: ")
    ui.appendST("(all / success / failed / percentage of success)")
    if(int(numOfAllocs) > 0):
        allocPercentage = str(round((float(sucAllocs) / float(numOfAllocs)) * 100,3))
        ui.appendST("Allocs: "+str(numOfAllocs)+" / "+str(sucAllocs)+" / "+str(int(numOfAllocs) - int(sucAllocs))+" / "+allocPercentage+"%")
    if(int(numOfFrees) > 0):
        freePercentage = str(round((float(sucFrees) / float(numOfFrees)) * 100,3))
        ui.appendST("Frees: "+str(numOfFrees)+" / "+str(sucFrees)+" / "+str(int(numOfFrees) - int(sucFrees))+" / "+freePercentage+"%")
    if (int(numOfReallocs) > 0):
        reallocPercentage = str(round((float(sucReallocs) / float(numOfReallocs)) * 100,3))
        ui.appendST("Reallocs: "+str(numOfReallocs)+" / "+str(sucReallocs)+" / "+str(int(numOfReallocs) - int(sucReallocs))+" /"+reallocPercentage+"%")
    ui.appendST("")
    ui.appendST("Memory utilization:")
    ui.appendST("Whole memory:  "+str(wholeMem)+"B")
    allocMemPercentage = str(round(((float(int(wholeMem) - int(remainingMem)) / float(wholeMem)) * 100),3))
    ui.appendST("Allocated memory:  "+str(int(wholeMem) - int(remainingMem))+"B  ("+str(allocMemPercentage)+" %)")
    freeMemPercentage = str(round(((float(remainingMem) / float(wholeMem)) * 100),3))
    ui.appendST("Free memory:  "+str(remainingMem)+"B  ("+str(freeMemPercentage)+" %)")
    ui.appendST("")
    #ui.appendST("Largest allocated block: "+str(maxAllocBlock)+"B")
    #ui.appendST("Smallest allocated block: "+str(minAllocBlock)+"B")
    #ui.appendST("Average allocatd block: " + str(averageAllocBlock) + "B")
    ui.appendST("Number of allocation fails due to external fagmentation: "+str(numOfExtFragFail))
    ui.setPB(allocMemPercentage)
    exportStatsToFile()


def exportStatsToFile():
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