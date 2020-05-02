import serial
import time
import struct
from os import system, name

ser = serial.Serial('COM8', 115200, timeout=0)

COMMAND_PACKET_SIZE = 22
SENSORS_PACKET_SIZE = 103

left_speed = 200
right_speed = 200
command = bytearray([0] * COMMAND_PACKET_SIZE)
sensors = bytearray([0] * SENSORS_PACKET_SIZE)
acc = [0 for x in range(6)]
gyro = [0 for x in range(6)]
magnetic_field = [0 for x in range(12)]
proximity = [0 for x in range(16)]
distance_cm = 0
mic_volume = [0 for x in range(8)]
battery_raw = 0
tv_remote_data = 0
selector = 0
button_state = 0
demo_state = 0


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

    # Set initial values for actuators


command[0] = 0xF8;  # -0x08: get all sensors
command[1] = 0xF7;  # -0x09: set all actuators
command[2] = 0;  # Settings: do not calibrate IR, disable onboard OA, set motors speed
command[3] = struct.unpack('<BB', struct.pack('<h', left_speed))[0]  # left motor LSB
command[4] = struct.unpack('<BB', struct.pack('<h', left_speed))[1]  # left motor MSB
command[5] = struct.unpack('<BB', struct.pack('<h', right_speed))[0]  # right motor LSB
command[6] = struct.unpack('<BB', struct.pack('<h', right_speed))[1]  # right motor MSB
command[7] = 0x3F;  # lEDs
command[8] = 0;  # LED2 red
command[9] = 0;  # LED2 green
command[10] = 0;  # LED2 blue
command[11] = 0;  # LED4 red
command[12] = 0;  # LED4 green
command[13] = 0;  # LED4 blue
command[14] = 0;  # LED6 red
command[15] = 0;  # LED6 green
command[16] = 0;  # LED6 blue
command[17] = 0;  # LED8 red
command[18] = 0;  # LED8 green
command[19] = 0;  # LED8 blue
command[20] = 0;  # speaker
command[21] = 0;  # End delimiter

start = time.time()

while (1):

    ser.write(command)
    sensors = ser.read()
    while len(sensors) < SENSORS_PACKET_SIZE:
        sensors += ser.read()

    # Accelerometer
    acc[0] = struct.unpack("<h", struct.pack("<BB", sensors[0], sensors[1]))[0]
    acc[1] = struct.unpack("<h", struct.pack("<BB", sensors[2], sensors[3]))[0]
    acc[2] = struct.unpack("<h", struct.pack("<BB", sensors[4], sensors[5]))[0]

    # Gyro
    gyro[0] = struct.unpack("<h", struct.pack("<BB", sensors[18], sensors[19]))[0]  # sensors[18] + sensors[19]*256
    gyro[1] = struct.unpack("<h", struct.pack("<BB", sensors[20], sensors[21]))[0]  # sensors[20] + sensors[21]*256
    gyro[2] = struct.unpack("<h", struct.pack("<BB", sensors[22], sensors[23]))[0]  # sensors[22] + sensors[23]*256

    # Magnetometer
    magnetic_field[0] = struct.unpack("<f", struct.pack("<BBBB", sensors[24], sensors[25], sensors[26], sensors[27]))[0]
    magnetic_field[1] = struct.unpack("<f", struct.pack("<BBBB", sensors[28], sensors[29], sensors[30], sensors[31]))[0]
    magnetic_field[2] = struct.unpack("<f", struct.pack("<BBBB", sensors[32], sensors[33], sensors[34], sensors[35]))[0]

    # Proximity sensors
    proximity[0] = sensors[37] + sensors[38] * 256
    proximity[1] = sensors[39] + sensors[40] * 256
    proximity[2] = sensors[41] + sensors[42] * 256
    proximity[3] = sensors[43] + sensors[44] * 256
    proximity[4] = sensors[45] + sensors[46] * 256
    proximity[5] = sensors[47] + sensors[48] * 256
    proximity[6] = sensors[49] + sensors[50] * 256
    proximity[7] = sensors[51] + sensors[52] * 256

    # Time of flight sensor
    distance_cm = (sensors[69] + sensors[70] * 256) / 10.0

    # Microphone
    mic_volume[0] = sensors[71] + sensors[72] * 256
    mic_volume[1] = sensors[73] + sensors[74] * 256
    mic_volume[2] = sensors[75] + sensors[76] * 256
    mic_volume[3] = sensors[77] + sensors[78] * 256

    # Battery
    battery_raw = sensors[83] + sensors[84] * 256

    # TV remote
    tv_remote_data = sensors[88]

    # Selector
    selector = sensors[89]

    # Button
    button_state = sensors[102]

    clear()
    print("acc: " + str(acc[0]) + ", " + str(acc[1]) + ", " + str(acc[2]))
    print("gyro: " + str(gyro[0]) + ", " + str(gyro[1]) + ", " + str(gyro[2]))
    print("magnetometer: " + str(magnetic_field[0]) + ", " + str(magnetic_field[1]) + ", " + str(magnetic_field[2]))
    print("prox: " + str(proximity[0]) + ", " + str(proximity[1]) + ", " + str(proximity[2]) + ", " + str(
        proximity[3]) + ", " + str(proximity[4]) + ", " + str(proximity[5]) + ", " + str(proximity[6]) + ", " + str(
        proximity[7]))
    print("distance (cm): " + str(distance_cm))
    print("microphone: " + str(mic_volume[0]) + ", " + str(mic_volume[1]) + ", " + str(mic_volume[2]) + ", " + str(
        mic_volume[3]))
    print("battery: " + str(battery_raw))
    print("tv remote: " + str(tv_remote_data))
    print("selector: " + str(selector))
    print("button: " + str(button_state))
    print()

    time_diff = time.time() - start
    if time_diff >= 3.0:
        start = time.time()
        if demo_state == 0:
            demo_state = 1
            left_speed = -200
            right_speed = -200
            command[3] = struct.unpack('<BB', struct.pack('<h', left_speed))[0]  # left motor LSB
            command[4] = struct.unpack('<BB', struct.pack('<h', left_speed))[1]  # left motor MSB
            command[5] = struct.unpack('<BB', struct.pack('<h', right_speed))[0]  # right motor LSB
            command[6] = struct.unpack('<BB', struct.pack('<h', right_speed))[1]  # right motor MSB
            command[7] = 0x00;  # lEDs
            command[8] = 100;  # LED2 red
            command[9] = 0;  # LED2 green
            command[10] = 0;  # LED2 blue
            command[11] = 0;  # LED4 red
            command[12] = 100;  # LED4 green
            command[13] = 0;  # LED4 blue
            command[14] = 0;  # LED6 red
            command[15] = 0;  # LED6 green
            command[16] = 100;  # LED6 blue
            command[17] = 100;  # LED8 red
            command[18] = 100;  # LED8 green
            command[19] = 100;  # LED8 blue
        elif demo_state == 1:
            demo_state = 0
            left_speed = 200
            right_speed = 200
            command[3] = struct.unpack('<BB', struct.pack('<h', left_speed))[0]  # left motor LSB
            command[4] = struct.unpack('<BB', struct.pack('<h', left_speed))[1]  # left motor MSB
            command[5] = struct.unpack('<BB', struct.pack('<h', right_speed))[0]  # right motor LSB
            command[6] = struct.unpack('<BB', struct.pack('<h', right_speed))[1]  # right motor MSB
            command[7] = 0x3F;  # lEDs
            command[8] = 0;  # LED2 red
            command[9] = 0;  # LED2 green
            command[10] = 0;  # LED2 blue
            command[11] = 0;  # LED4 red
            command[12] = 0;  # LED4 green
            command[13] = 0;  # LED4 blue
            command[14] = 0;  # LED6 red
            command[15] = 0;  # LED6 green
            command[16] = 0;  # LED6 blue
            command[17] = 0;  # LED8 red
            command[18] = 0;  # LED8 green
            command[19] = 0;  # LED8 blue

ser.close()
