import serial
import os
from flask import Flask, request

serial_ports = {'system0': os.getenv("SERIAL_PORT")}
baud_rate = 9600

app = Flask(__name__)

# Define routes
@app.route('/configure', methods=['GET', 'POST'])
def configure():
    data = request.get_json()
    print("Received configuration data:", data)

    ser = serial.Serial(serial_ports['system0'], baud_rate)
    ser.write(data['min_temperature'])
    ser.write(b'\n')
    ser.write(data['max_temperature'])
    ser.write(b'\n')
    ser.write(data['min_humidity'])
    ser.write(b'\n')
    ser.write(data['max_humidity'])
    ser.write(b'\n')

    return 'Sensor configured successfully'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
