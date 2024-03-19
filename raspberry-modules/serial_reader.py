import serial
import os
import sys
import requests

serial_port = os.getenv("SERIAL_PORT")
server_url = os.getenv("SERVER_URL") or "127.0.0.1:5001"
baud_rate = 9600

print(f"Server URL: {server_url}")

# Initialize the serial connection
ser = serial.Serial(serial_port, baud_rate)
ser.flush()

try:
    while True:
        # Read a line from the serial port
        line = ser.readline().decode("utf-8").strip()
        info = line.split()

        if info[0] == "warning":
            print(line)
            requests.post('http://' + server_url + '/notify', data={'sensorid': info[1], 'value': info[2]})
        elif info[0] == "measurement":
            print(info)
            requests.post('http://' + server_url + '/addMeasure', data={'sensorid': info[1], 'value': info[2]})
        elif info[0] == "error":
            print(line)
        else:
            raise ValueError("This should never happen!")

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()  # Close the serial connection when the program exits
