import RPi.GPIO as GPIO
import datetime
import time
from adafruit_servokit import ServoKit

channel_num = 16
kit = ServoKit(channels=channel_num)
for i in range(channel_num):
    kit.servo[i].actuation_range = 180
    kit.servo[i].angle = 0
    kit.servo[i].set_pulse_width_range(750, 2650)

def apply_to_all_servos(num_servos, value, raw_angle=False):

    for i in range(num_servos):
        if raw_angle:
            kit.servo[i].angle = int(value)
        else:
            kit.servo[i].angle = value * 20

mode = input("1. Manual Degrees Mode\n2. Continuous Counting Mode\n")
if mode == "1":
    while True:
        angle = input("Which angle do you want?\n")
        if angle.isdigit():
            apply_to_all_servos(4, angle, True)
elif mode == "2":
    number = 0
    increasing = True
    while True:

        if increasing:
            number += 1
        else:
            number -= 1

        apply_to_all_servos(4, number, False)

        if number == 0:
            increasing = True
            time.sleep(5)
        else:
            if number == 9:
                increasing = False
                time.sleep(5)
            else:
                time.sleep(1.5)
else:
    print("No such option")
