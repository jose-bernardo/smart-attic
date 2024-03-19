import serial
import os
import requests

serial_ports = {'user1': os.getenv("SERIAL_PORT")}
server_url = os.getenv("SERVER_URL") or "127.0.0.1:5001"
server_url = 'http://' + server_url if not server_url.startswith('http://') else server_url
print(server_url)
baud_rate = 9600

print(f"Server URL: {server_url}")

try:
    while True:
        # Initialize the serial connection
        ser = serial.Serial(serial_ports['user1'], baud_rate)
        ser.flush()
        # Read a line from the serial port
        line = ser.readline().decode("utf-8").strip()
        info = line.split()
        print(line)

        # TODO user should be passed according to sensor
        if info[0] == "warning":
            requests.post(server_url + '/notify', data={'sensorid': info[1], 'value': info[2], 'username': serial_ports['user1']})
        elif info[0] == "measurement":
            requests.post(server_url + '/addMeasure', data={'sensorid': info[1], 'value': info[2]})

        ser.close()  # Close the serial connection when the program exits
except KeyboardInterrupt:
    print("Exiting...")
