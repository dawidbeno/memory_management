import serial
import time
import sys
from PyQt4 import QtCore, QtGui


# **** IMPORTANT ****
# Strings that Arduino send with println function, ends with "\r\n"

#config
ALGORITHM = "best"
ser = None
test = ""

# Creates connection with COM3 port
def init():
    global ser
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(1)
        var = ser.readline()
        ser.write(b'i')
        while 1:
            time.sleep(1)
            var = ser.readline()
            if(var == "INIT\r\n"):
                print "init successful"
                break
            else:
                print "waiting for init ..."
    except Exception:
        print "COM3 serial port not found"




# sets algorithm which will be used by tests
def setalg(algType):
    global ALGORITHM
    global ser

    if(algType == "best"):
        ser.write(b'b')
        while True:
            var = ser.readline()
            if(var.__contains__("Alg changed to:")):
                var2 = var.split(':')[1]
                var = var2[0]
                if(var == 'b'):
                    ALGORITHM = "BEST"
                    print "Set alg to BEST"
                    break
            print "waiting to set algorithm ..."
            time.sleep(1)

    elif(algType == "worst"):
        ser.write(b'w')
        while True:
            var = ser.readline()
            if (var.__contains__("Alg changed to:")):
                var2 = var.split(':')[1]
                var = var2[0]
                if(var == 'w'):
                    ALGORITHM = "WORST"
                    print "Set alg to WORST"
                    break
            print "waiting to set algorithm ..."
            time.sleep(1)

    else:
        print "Bad type of algorithm"
        print "Type \"help\" for more info"



# Load test
def loadTest(testLvl):
    global test
    test = "tests\\level_" + testLvl
    # try:
    #     file = open(str, "r")
    #     test = str
    #     print file.read()
    # except Exception:
    #     print "Bad level chosed or no file found"




def testAlloc(size):
    global ser
    print "Start test allocation"
    ser.write(b'a')
    # serial.write(len(size)) NEFUNGUJE a neviem preco :(
    if(len(size) == 1):
        ser.write(b'1')
    elif(len(size) == 2):
        ser.write(b'2')
    elif(len(size) == 3):
        ser.write(b'3')
    elif(len(size) == 4):
        ser.write(b'4')
    ser.write(size)
    while True:
        line = ser.readline()
        if(line.__contains__("SUCCESS") or line.__contains__("FAILED")):
            print line
            break
        print line
        time.sleep(1)


def testFree(ptr):
    global ser
    print "Start test free"
    ser.write(b'f')
    if (len(ptr) == 1):
        ser.write(b'1')
    elif (len(ptr) == 2):
        ser.write(b'2')
    elif (len(ptr) == 3):
        ser.write(b'3')
    elif (len(ptr) == 4):
        ser.write(b'4')
    ser.write(ptr)
    while True:
        line = ser.readline()
        if(line.__contains__("Free complete")):
            print line
            break
        print line
        time.sleep(1)

# must be loaded first
def startTest():
    global test
    print "Start testovania"
    print test
    with open(test, "r") as f:
        for line in f:
            print line



def showMemoryState():
    global ser
    print "ACTUAL MEMORY STATE"
    ser.write(b'p')
    while True:
        line = ser.readline()
        print line
        if(line.__contains__("Finish")):
            break
        time.sleep(1)


# Prints help to stdout
def help():
    global ALGORITHM
    file = open("help.txt", "r")
    print file.read()
    print "ACTUAL CONFIG:"
    print "Algorithm: %s" % ALGORITHM




def main():
    print ""
    print "***********************************************"
    print "     MEMORY ALLOCATION TESTING PROGRAM"
    print "     Type \"help\" for more info"
    print "***********************************************"
    print ""
    init()
    global ALGORITHM
    global ser

    # Main loop, waiting for command
    while(True):
        cmd = raw_input("\n("+ALGORITHM+") cmd> \n")
        if(cmd == "help"):
            help()
        elif(cmd.__contains__("setalg")):
            try:
                algtype = cmd.split(' ')[1]
                setalg(algtype)
            except Exception:
                print "No algorithm chosed"
                print "Undefined command, type \"help\" for more info"
        elif(cmd.__contains__("load")):
            try:
                testLvl = cmd.split(' ')[1]
                loadTest(testLvl)
            except Exception:
                print "No test level chosed"
                print "Undefined command, type \"help\" for more info"
        elif(cmd.__contains__("start")):
            startTest()
        elif(cmd.__contains__("showmem")):
            showMemoryState()
        elif(cmd.__contains__("alloc")):
            try:
                space = cmd.split(' ')[1]
                testAlloc(space)
            except Exception:
                print "No spece requested"
                print "Undefined command, type \"help\" for more info"
        elif(cmd.__contains__("free")):
            try:
                addr = cmd.split(' ')[1]
                testFree(addr)
            except Exception:
                print "Bad free"
                print "Undefined command, type \"help\" for more info"
        elif(cmd == "q"):
            print ""
            print "Exit testing program"
            exit()
        else:
            print "Undefined command, type \"help\" for more info"


main()


