import RPi.GPIO as GPIO
import random
import time


class diceRoller:

    def __init__(self):

        GPIO.setmode(GPIO.BOARD)

        # Digits
        pin_tens = 15
        GPIO.setup(pin_tens, GPIO.OUT)
        self.tens = GPIO.PWM(pin_tens, 50)
        self.tens.start(0)

        pin_ones = 16
        GPIO.setup(pin_ones, GPIO.OUT)
        self.ones = GPIO.PWM(pin_ones, 50)
        self.ones.start(0)

    # Function to set servo angle
    def set_angle(self, servo, angle):
        duty_cycle = 2 + (angle / 18)
        servo.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)

    def set_servos(self, amount, max_value):
        position_translation_dict = {
            "0": 00,
            "1": 18,
            "2": 36,
            "3": 54,
            "4": 72,
            "5": 90,
            "6": 108,
            "7": 126,
            "8": 144,
            "9": 162,
            }
        value = int(amount) * random.randint(1, int(max_value))
        if value <= 99:
            self.set_angle(self.tens, position_translation_dict[str(value)[0]])
            self.set_angle(self.ones, position_translation_dict[str(value)[-1]])
            print(f"Results: {value}")
        else:
            print("Error: Value too high, limited to two digits")
if __name__ == '__main__':
        dice_rollder_obj = diceRoller()
        try:
            while True:
                dice = input("What dice do you want to roll? <xdx format>\n")
                amount, max_value = dice.split("d")
                if amount.isdigit() and max_value.isdigit():
                    dice_rollder_obj.set_servos(amount, max_value)
        except KeyboardInterrupt:
            # Clean up on exit
            dice_rollder_obj.tens.stop()
            dice_rollder_obj.ones.stop()
            GPIO.cleanup()
