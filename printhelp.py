import serial
import time
ser = serial.Serial('COM5', 115200, timeout=0)

ser.write(bytes(b'H\r\n'))
time.sleep(1)
print(ser.read(1000))

ser.close()