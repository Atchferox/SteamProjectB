import time
import RPi.GPIO as GPIO

# RGB LED pinnen configureren.
pinBlauw = 16
pinGroen = 20
pinRood = 21

# GPIO setup.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Zet de GPIO pinnen als uitgang.
GPIO.setup(pinRood, GPIO.OUT)
GPIO.setup(pinGroen, GPIO.OUT)
GPIO.setup(pinBlauw, GPIO.OUT)


GPIO.output(pinRood, GPIO.HIGH)
GPIO.output(pinGroen, GPIO.HIGH)
GPIO.output(pinBlauw, GPIO.HIGH)


