import serial
import time
import struct
ser = serial.Serial('COM6', 115200, timeout=0)

message = struct.pack(">bb", - ord('N'), 0)
ser.write(message)
print("write")
reply = ser.read()
print("reply")

while len(reply) < 16: # Each sensor is 2 bytes.

	reply += ser.read()

reply = struct.unpack('@HHHHHHHH', reply)
print("prox: " + str(reply[0]) + ", " + str(reply[1]) + ", " + str(reply[2]) + ", " + str(reply[3]) + ", " + str(reply[4]) + ", " + str(reply[5]) + ", " + str(reply[6]) + ", " + str(reply[7]))

ser.close()

# 카메라를 12시방향으로 두고 시계방향으로 0~7까지 근접센서 번호가 매겨집지다.
# 근접센서의 경우 너무 근접하게 되면 세마포 초과 오류가 발생하고 근접할수록 수가 점점 큰폭으로 커집니다
