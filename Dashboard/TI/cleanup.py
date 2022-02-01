import RPi.GPIO as GPIO

pinBlauw = 16
pinGroen = 20
pinRood = 21
LCD_RS = 26
LCD_E = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 22
kill_switch = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.cleanup()