import argparse
import datetime
import math
import time
import os
import pathlib

from playsound import playsound
from adafruit_servokit import ServoKit


class piClock:

    def __init__(self):
        
        # Initialize the servo bonnet kit and start at zero
        channel_num = 16
        kit = ServoKit(channels=channel_num)
        for i in range(channel_num):
            kit.servo[i].set_pulse_width_range(750, 2650)
            kit.servo[i].actuation_range = 180
            self.set_angle(kit.servo[i], 0)

            # Only 6 servos will ever be needed
            if i == 5:
                break
            # Too much power draw if all servos are moving at once
            time.sleep(1)

        # Hours
        self.hours_tens = kit.servo[0]
        self.hours_ones = kit.servo[1]

        # Minutes
        self.minutes_tens = kit.servo[2]
        self.minutes_ones = kit.servo[3]

        # Seconds
        # self.seconds_tens = kit.servo[4]
        # self.seconds_ones = kit.servo[5]

        self.stored_hour = 00
        self.stored_minute = 00

    def set_angle(self, servo: ServoKit, number: int) -> None:
        """ 
        Take a given number and set the servo to that angle. 
        Since 180/20 = 9 we can simplify the angles with a simple multiplication
        @param servo: The specific servo to adjust the current signal on
        @param number: The number, 0-9, to display in a specific servo
        """

        if not servo.angle:
            servo.angle = 0
        current_number = math.ceil(servo.angle)

        # Increment the servo angle over time
        if current_number < number*20:
            iteratator = 1
        else:
            iteratator = -1
        
        for i in range(current_number, (number*20)+iteratator, iteratator):
            servo.angle = i
            time.sleep(.05)

    def set_servos(self, hour: int, minute: int) -> None:
        """ Parse the hours and minutes to send as servo angles 
        Cycle right to left so when only the minute is change it happens on top of the minute
        @param hours: The current hour
        @param minutes: The current minute
        """

        # Only change a server if the new time is different
        if (minute % 10) != (self.stored_minute % 10):
            self.set_angle(self.minutes_ones, minute % 10)
        if (minute % 100 // 10) != (self.stored_minute % 100 // 10):
            self.set_angle(self.minutes_tens, minute % 100 // 10)

        self.stored_minute = minute

        if (hour % 10) != (self.stored_hour % 10):
            self.set_angle(self.hours_ones, hour % 10)
        if (hour % 100 // 10) != (self.stored_hour % 100 // 10):
            self.set_angle(self.hours_tens, hour % 100 // 10)

        self.stored_hour = hour
    
        
def dynamic_sleep() -> int:
    """ 
    Calculate the specific seconds to sleep for based on when the next xx:xx:00 time stamp is. 
    This prevents drift and ensures time changes at the top of the minute
    @return: number of seconds to sleep for
    """
    sleep_time = 60 - datetime.datetime.now().second
    return sleep_time

def announce_time(curent_time: datetime) -> None:
    """ 
    Read out the time to the speaker 
    @param current_time: datetime now
    """

    sound_file = os.path.join(pathlib.Path(__file__).parent.resolve(), "sound_files", f"{str(curent_time.hour)}.wav")

    if os.path.isfile(sound_file):
        playsound(sound_file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Pi Servo Mechanical Clock')

    parser.add_argument('-l', "--limit-changes", action="store_true", help='Limit the amount of time changes outside of waking hours')
    args = parser.parse_args()

    pi_clock_obj = piClock()
    # Wait for the top of the second to start keeping time
    sleep_time = dynamic_sleep()
    print(f"Waiting till the top of the second. Sleeping for {sleep_time} seconds")
    time.sleep(sleep_time)
    recorded_hour = 00
    while True:
        now = datetime.datetime.now()
        print(now)
        # Only change the hour servos when sleeping
        if args.limit_changes and (2 <= now.hour <= 8):
            pi_clock_obj.set_servos(now.hour, 00)
        else:
            # Send the current hour and minute with leading zeros
            pi_clock_obj.set_servos(now.hour, now.minute)

        # Vocalize the current hour if the hour has changed
        if now.hour != recorded_hour:
            announce_time(now)
            recorded_hour = now.hour
        time.sleep(dynamic_sleep())
