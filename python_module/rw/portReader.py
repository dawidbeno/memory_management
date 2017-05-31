import serial
import time

ser = serial.Serial('/dev/tty.usbmodem1421', 9600)

while 1:
    try:
        var = ser.readline()
        if(var):
            print(var)
        time.sleep(1)
    except ser.SerialTimeoutException:
        print('Data could not be read')
        time.sleep(1)



