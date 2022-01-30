import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

kill_switch = 12

GPIO.setup(kill_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#als knop ingedrukt is sluit pi af
while True:
    if GPIO.input(kill_switch):
        os.system("sudo shutdown now -h")
        print("Pc is DIE")
