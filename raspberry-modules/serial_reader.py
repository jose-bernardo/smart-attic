import serial
import os

#serial_port = os.getenv("SERIAL_PORT")
serial_port = "/dev/tty.usbmodem101"
baud_rate = 9600

# Initialize the serial connection
ser = serial.Serial(serial_port, baud_rate)

try:
    while True:
        # Read a line from the serial port
        line = ser.readline().decode("utf-8").strip()
        print(line)
except KeyboardInterrupt:
    print("Exiting...")
    ser.close()  # Close the serial connection when the program exits
