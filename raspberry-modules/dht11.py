import time
import adafruit_dht
import board
import RPi.GPIO as GPIO

dht_device = adafruit_dht.DHT11(board.D4)

hum_led_pin_red = 17
hum_led_pin_green = 27
hum_led_pin_blue = 22

temp_led_pin_red = 10
temp_led_pin_green = 9
temp_led_pin_blue = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# setup temperature rgb led
GPIO.setup(temp_led_pin_red, GPIO.OUT)
GPIO.setup(temp_led_pin_green, GPIO.OUT)
GPIO.setup(temp_led_pin_blue, GPIO.OUT)

# setup humidity rgb led
GPIO.setup(hum_led_pin_red, GPIO.OUT)
GPIO.setup(hum_led_pin_green, GPIO.OUT)
GPIO.setup(hum_led_pin_blue, GPIO.OUT)

while True:
    try:
        temperatuce_c = dht_device.temperature
        humidity = dht_device.humidity

        if 15 < temperatuce_c < 25:
            GPIO.output(temp_led_pin_red, GPIO.HIGH)
            GPIO.output(temp_led_pin_green, GPIO.LOW)
            GPIO.output(temp_led_pin_blue, GPIO.HIGH)
        else:
            # simulate to answer the problem
            GPIO.output(temp_led_pin_red, GPIO.LOW)
            GPIO.output(temp_led_pin_green, GPIO.HIGH)
            GPIO.output(temp_led_pin_blue, GPIO.HIGH)

            # send notification request to the central hub
            # TODO

        if 30 < humidity < 60:
            GPIO.output(hum_led_pin_red, GPIO.HIGH)
            GPIO.output(hum_led_pin_green, GPIO.LOW)
            GPIO.output(hum_led_pin_blue, GPIO.HIGH)
        else:
            # simulate to answer the problem
            GPIO.output(hum_led_pin_red, GPIO.LOW)
            GPIO.output(hum_led_pin_green, GPIO.HIGH)
            GPIO.output(hum_led_pin_blue, GPIO.HIGH)

            # send notification request to the central hub
            # TODO

        print(f"Temperature:{temperatuce_c:.1f} C\nHumidity:{humidity}%")
    except RuntimeError as e:
        print("failed to read data from dht11 sensor:", e)

    time.sleep(2.0)
