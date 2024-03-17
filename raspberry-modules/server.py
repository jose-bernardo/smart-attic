from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receiveAlarmValues', methods=['POST'])
def receiveAlarmValues():
    data = request.json  # Extract JSON data from the request
    min_humidity = data.get('minHumidity')
    max_humidity = data.get('maxHumidity')
    min_temperature = data.get('minTemperature')
    max_temperature = data.get('maxTemperature')

    # TODO Do something with the received data
    # For demonstration purposes, we will just print it
    print("Min Humidity:", min_humidity)
    print("Max Humidity:", max_humidity)
    print("Min Temperature:", min_temperature)
    print("Max Temperature:", max_temperature)

    # Return a response indicating success
    return jsonify({'message': 'Data received successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)