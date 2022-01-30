import time
import RPi.GPIO as GPIO
import requests

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

def offline():
    try:
        while True:
            #haal onlinestatus uit steam API
            response = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=F7CD5F6E51D9114EC9D9C44EEBCA6FF7&steamids=76561198208819849")
            data = response.json()
            userstatus = data["response"]["players"][0]["personastate"]
            print(userstatus)

            Offline = userstatus == 0
            Online = userstatus == 1
            Busy = userstatus == 2
            Away = userstatus == 3
            Snooze = userstatus == 4
            looking_to_trade = userstatus == 5
            looking_to_play = userstatus == 6

            #als user offline led gaat uit
            while Offline:
                GPIO.output(pinRood, GPIO.LOW)
                GPIO.output(pinGroen, GPIO.LOW)
                GPIO.output(pinBlauw, GPIO.LOW)
                break
            time.sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()


offline()
