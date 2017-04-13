import serial
import time


TEST_DIR = "/home/dejvid/BP/Codes/memory_management/python_module/src/tests/"
serialComm = None

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
                ui.appendMV("init successful")
                break
            else:
                print "waiting for init ..."
    except Exception:
        print "Serial port not found"


def load_1():
    file = open(TEST_DIR+"level_1", "r")
    return file.read()

def load_2():
    file = open(TEST_DIR+"level_2", "r")
    return file.read()

def load_3():
    file = open(TEST_DIR+"level_3", "r")
    return file.read()

def load_4():
    file = open(TEST_DIR+"level_4", "r")
    return file.read()


def nextStep(step, ui):
    result = step + " Complete"
    ui.appendMV("NEXT STEp")
    return result