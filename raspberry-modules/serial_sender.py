import serial
import os
from flask import Flask, request

serial_ports = {'user1': os.getenv("SERIAL_PORT")}
baud_rate = 9600

app = Flask(__name__)

# Define routes
@app.route('/configure', methods=['POST'])
def configure():
    data = request.get_json()
    print("Received configuration data:", data)

    ser = serial.Serial(serial_ports['user1'], baud_rate)
    ser.write('config'.encode())
    ser.write(b'\n')
    ser.write(data['minTemperature'].encode())
    ser.write(b'\n')
    ser.write(data['maxTemperature'].encode())
    ser.write(b'\n')
    ser.write(data['minHumidity'].encode())
    ser.write(b'\n')
    ser.write(data['maxHumidity'].encode())
    ser.write(b'\n')
    ser.close()

    return 'Sensor configured successfully'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
