import serial
import time

ser = serial.Serial('COM3', 9600, timeout=0)
var = raw_input("Enter something: ")
ser.write(var)

while 1:
    try:
        var = ser.readline()
        if (var):
            print(var)
        time.sleep(1)
    except ser.SerialTimeoutException:
        print('Data could not be read')