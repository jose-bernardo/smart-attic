import RPi.GPIO as GPIO
import time

photoresistor_pin = 5
led_pin = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(read_pin,GPIO.IN)
GPIO.setwarnings(True)

while True:
    try:
        ambient_light = GPIO.input(photoresistor_pin)
        print(f"Light:{ambient_light}")

        if ambient_light > 500:
            GPIO.output(led_pin, GPIO.HIGH)
            print("Dangerous light leak!")

            # send notification request to central hub
            # TODO
        else:
            GPIO.output(led_pin, GPIO.LOW)
    except KeyboardInterrupt as e:
        GPIO.cleanup()
        print("failed to read data from from photoresistor:", e)

    time.sleep(2.0)
