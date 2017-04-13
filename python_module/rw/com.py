import time
import serial

ser = serial.Serial('COM3', 9600)

time.sleep(1)
print ser.readline()
#time.sleep(1)
# print ser.readline()
# time.sleep(3)
# print ser.readline()
# time.sleep(3)
# print ser.readline()
# time.sleep(3)

ser.write(b'a')
ser.write(b'3')
ser.write(b'eui')
#ser.write(b'r')
#ser.write(b't')

ser.write(b'w')
#time.sleep(1)

print ser.readline()
time.sleep(1)
print ser.readline()
time.sleep(1)
print ser.readline()
time.sleep(1)
print ser.readline()
time.sleep(3)

ser.write(b'b')
time.sleep(1)

print ser.readline()
time.sleep(1)
print ser.readline()
time.sleep(1)
print ser.readline()
time.sleep(1)
print ser.readline()
time.sleep(1)
print ser.readline()
time.sleep(1)
print ser.readline()
time.sleep(1)

print ser.readline()
time.sleep(1)
print ser.readline()
time.sleep(1)