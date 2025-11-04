import RPi.GPIO as GPIO # type: ignore

from time import sleep

class HeartbeatLed:
    def __init__(self, pin):
        self.pin = pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
    
    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def blink(self, duration=0.1):
        self.turn_on()
        sleep(duration)
        self.turn_off()