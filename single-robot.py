import serial
# This script open a connection with 2 robots and exchanged data with them using the "advanced sercom protocol".
# Tested with Python 3.4
# Requirements: PySerial module.

import time
import struct

robot1 = serial.Serial('COM6', 115200, timeout=0)  # Specify the robot communication port (after pairing).

# Robot 1 actuators state.
rob1_leds = bytearray([0, 0, 0, 0, 0, 0, 0, 0])
rob1_left_speed = -500
rob1_right_speed = 500
#LED와 왼쪽 오른쪽 스피드에 대한 변수선언

while (1):
    # Prepare the message to send to robot1.
    left = struct.unpack('bb', struct.pack('h', rob1_left_speed))
    #왼쪽바퀴에 변수에 저장된 값 입력
    right = struct.unpack('bb', struct.pack('h', rob1_right_speed))
    #오른쪽바퀴에 변수에 저장된 값 입력
    #left랑 right가 두칸짜리 배열이되어서 나왔다 : bb
    message = struct.pack("<bbbbbbbbbbbbb", - ord('a'), - ord('N'), - ord('g'), - ord('u'), - ord('L'), 0, rob1_leds[0],
                          - ord('D'), left[0], left[1], right[0], right[1], 0)
    #로봇에게 전달할 매세지를 만든다 pack이용해서 b가 13개이고 뒤에 파라미터가 13개가 입력된다
    # 파라미터 값이 양수면 ASCII, 음수면 Binary
    # -ord('a') 가속도계 축값 얻기
    # -ord('N') 근접센서 값 얻기
    # -ord('g') 자이로 3축값 가져오기
    # -ord('u') 마이크 진폭값 얻기그냥
    # -ord('L') LED상태 설정
    # 0
    # rob1_leds[0]
    # -ord('D') 모터 속도 설정
    # left[0] left의 LSB
    # left[1] left의 MSB
    # right[0] right의 LSB
    # right[1] right의 MSB
    # 0

    robot1.write(message)
    #.write이용해서 메세지 로봇에게 전달
    #일단은 로봇에 대해서 init하는 것으로 파악됨

    # Read the expected data from robot1.
    reply = robot1.read()
    while len(reply) < 34:
        reply += robot1.read()
    #응답을 주고 reply를 받아온다 34바이트가 넘으면 loop종료

    # Extract the sensors data.
    rob1_acc = struct.unpack('@hhh', reply[0:6])
    #-ord('a')에 대한 응답 배열7자리, h 3개
    rob1_prox = struct.unpack('@HHHHHHHH', reply[6:22])
    # -ord('N')에 대한 응답 17자리 H 8개
    rob1_gyro = struct.unpack('@hhh', reply[22:28])
    # -ord('g')에 대한 응답 7자리 h 3개
    rob1_micro = struct.unpack('@HHH', reply[28:34])
    #-ord('u')에 대한 응답 7자리 H 3개
    print("\r\nrob1")
    print("acc0: " + str(rob1_acc[0]))
    print("prox0: " + str(rob1_prox[0]))
    print("gyro0: " + str(rob1_gyro[0]))
    print("micro0: " + str(rob1_micro[0]))

robot1.close()
