from flask import Flask, render_template, request, redirect, session, url_for, Response
from flask_mail import Mail, Message
from functools import wraps
import requests
import secrets
import mariadb
import plotly.graph_objs as go
import time, datetime
import os
import random

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='cocodoce02@gmail.com', # Change this maybe :))))) Your Gmail address
    MAIL_PASSWORD='aocb lgki dmgj yzkj',  # Your Gmail app password
    MAIL_DEFAULT_SENDER='cocodoce02@gmail.com'  # Default sender email
)
mail = Mail(app)

config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

pool = mariadb.ConnectionPool(
    pool_name='smartatticpool',
    pool_size=5,
    **config
)

# Placeholder user credentials (replace with secure storage but its ok for simulation)
users = {'user1': 'user1'}
emails = {'user1': os.getenv('MAIL_ADDRESS')}
pins = {'user1': None}
app.secret_key = secrets.token_hex(16)  # Generates a 32-character hexadecimal string (16 bytes)

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if not session.get('logged_in'):
      return redirect(url_for('login'))
    return f(*args, **kwargs)
  return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if session.get('logged_in'):
      # User already logged in
      return redirect('/')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            # Successful login (replace with redirection to protected area)
            session['logged_in'] = True
            session['username'] = username
            return redirect('/')
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET'])
@login_required
def logout():    
    del session['logged_in']
    del session['username']
    return redirect('/login')

@app.route('/changeAlarmValues', methods=['GET', 'POST'])
@login_required
def changeAlarmValues():

    if request.method == 'POST':
        #min_humidity = request.form.get('minHumidity') or ''
        #max_humidity = request.form.get('maxHumidity') or ''
        #min_temperature = request.form.get('minTemperature') or ''
        #max_temperature = request.form.get('maxTemperature') or ''

        min_humidity = request.form.get('minHumidity')
        max_humidity = request.form.get('maxHumidity')
        min_temperature = request.form.get('minTemperature')
        max_temperature = request.form.get('maxTemperature')

        humidity_error_min = None
        humidity_error_max = None
        temperature_error_min = None
        temperature_error_max = None

        if min_humidity != '':
            if not min_humidity.isdigit() or not 20 <= int(min_humidity) <= 95:
                humidity_error_min = 'Min humidity must be a number between 20 and 95'
        if max_humidity != '':
            if not max_humidity.isdigit() or not 20 <= int(max_humidity) <= 95:
                humidity_error_max = 'Max humidity must be a number between 20 and 95'

        if min_temperature != '':
            if not min_temperature.isdigit() or not 0 <= int(min_temperature) <= 50:
                temperature_error_min = 'Min temperature must be a number between 0 and 50'
        if max_temperature != '':
            if not max_temperature.isdigit() or not 0 <= int(max_temperature) <= 50:
                temperature_error_max = 'Max temperature must be a number between 0 and 50'

        if humidity_error_min or humidity_error_max or temperature_error_min or temperature_error_max:
            return render_template('changeAlarmValues.html',
                                   humidity_error_min=humidity_error_min,
                                   humidity_error_max=humidity_error_max,
                                   temperature_error_min=temperature_error_min,
                                   temperature_error_max=temperature_error_max
                                   )

        # Data to send to the other Flask app
        data = {
                'minHumidity': min_humidity,
                'maxHumidity': max_humidity,
                'minTemperature': min_temperature,
                'maxTemperature': max_temperature
                }

        url = 'http://' + (os.getenv('PI_ADDRESS') or '127.0.0.1:5002') + '/configure'

        # Make a POST request to the other Flask app
        response = requests.post(url, json=data)

        # Check if the request was successful
        if response.ok:
            return 'Values were changed successfully'
        else:
            return 'Something went wrong', 500

    return render_template('changeAlarmValues.html')



@app.route('/getPin', methods=['GET'])
@login_required
def get_pin():
    # Generate a random integer between 1000 and 9999 (inclusive)
    pin = random.randint(1000, 9999)\
    
    pins[session['username']] = (pin, time.time() + 10)

    return render_template('getpin.html', pin=pin)


@app.route('/analytics', methods=['GET', 'POST'])
@login_required
def analytics():
    if ('start_date' in request.form and 'end_date' in request.form):
        start_date = request.form['start_date']
        end_date = request.form['end_date']
    else:
        start_date = datetime.datetime.now() - datetime.timedelta(hours=24)
        end_date = datetime.datetime.now()
        start_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
        end_date = end_date.strftime('%Y-%m-%d %H:%M:%S')

    conn = pool.get_connection()
    cur = conn.cursor()
    cur.execute('SELECT VALUE, MEASURE_TIMESTAMP FROM MEASUREMENTS ' + 
                'WHERE SENSORID=\'temperature\' AND MEASURE_TIMESTAMP BETWEEN %s AND %s', (start_date, end_date))
    conn.commit()
    temperature_values = []
    timestamps = [] 
    for value, timestamp in cur:
        temperature_values.append(value)
        timestamps.append(timestamp)

    # Create temperature graph
    trace = go.Scatter(x=timestamps, y=temperature_values, mode='lines+markers', name='Humidity')
    layout = go.Layout(title='Temperature Over Time',
                       xaxis=dict(title='Time'),
                       yaxis=dict(title='Temperature (°C)'))
    fig = go.Figure(data=[trace], layout=layout)
    temperature_graph_json = fig.to_json()

    cur.execute('SELECT VALUE, MEASURE_TIMESTAMP FROM MEASUREMENTS ' + 
                'WHERE SENSORID=\'humidity\' AND MEASURE_TIMESTAMP BETWEEN %s AND %s', (start_date, end_date))
    humidity_values = []
    timestamps = []
    for value, timestamp in cur:
        humidity_values.append(value)
        timestamps.append(timestamp)

    cur.close()
    conn.close()

    # Create humidity graph
    trace = go.Scatter(x=timestamps, y=humidity_values, mode='lines+markers', name='Humidity')
    layout = go.Layout(title='Humidity Over Time',
                       xaxis=dict(title='Time'),
                       yaxis=dict(title='Humidity (%)'))
    fig = go.Figure(data=[trace], layout=layout)
    humidity_graph_json = fig.to_json()

    return render_template('analytics.html', data={'humidity': humidity_graph_json, 'temperature': temperature_graph_json})

@app.route('/', methods=['GET'])
@login_required
def main():
    conn = pool.get_connection()
    cur = conn.cursor()
    cur.execute('SELECT VALUE, MEASURE_TIMESTAMP FROM MEASUREMENTS ' + 
                'WHERE SENSORID=\'temperature\' ORDER BY MEASURE_TIMESTAMP DESC LIMIT 1')
    conn.commit()

    temperature, timestamp = cur.fetchone()
    cur.close()

    cur = conn.cursor()
    cur.execute('SELECT VALUE, MEASURE_TIMESTAMP FROM MEASUREMENTS ' + 
                'WHERE SENSORID=\'humidity\' ORDER BY MEASURE_TIMESTAMP DESC LIMIT 1')
    conn.commit()

    humidity, timestamp = cur.fetchone()
    cur.close()
    conn.close()

    data = {
            "temperature": temperature,
            "humidity": humidity,
            "luminosity": "GOOD",
            "waterLeaks": "No leaks detected",
            "timestamp": timestamp,
            }

    return render_template('main.html', data=data)

@app.route('/addMeasure', methods=['POST'])
def addMeasure():
    value = request.form['value']
    sensorid = request.form['sensorid']
    if not sensorid or not value:
        return Response(status=400)

    try:
        conn = pool.get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO MEASUREMENTS (VALUE, SENSORID) VALUES (?, ?)", (float(value), sensorid))
        conn.commit()
        cur.close()
        conn.close()
    except mariadb.Error as e:
        print(e)

    return Response(status=200)

@app.route('/addFootage', methods=['POST'])
def addFootage():
    # Receive the video file from the server
    videofile = request.files['video']
    username = request.json['username']
    filename = './media/video_' + str(time.time()) + '.avi'
    videofile.save(filename)

    # for testing purposes 
    #filename = './media/received_video1710517031.731575.avi'

    recipient_email = emails[username]
    subject = "Video footage for invalid pin input"
    body = "Please see the attached video footage."

    msg = Message(subject, recipients=[recipient_email])
    msg.body = body

    # Attach the video file to the email
    with app.open_resource(filename) as video:
        msg.attach('video.avi', 'video/avi', video.read())

    try:
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return str(e), 500

@app.route('/notify', methods=['POST'])
def notify():
    username = request.json['username']
    recipient_email = emails[username]
    subject = "Alarm " + request.form['sensorid']
    body = "Alarm for " + request.form['sensorid'] + " sensor. Value: " + request.form['value']

    msg = Message(subject, recipients=[recipient_email])
    msg.body = body
    try:
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return str(e), 500
    
@app.route('/enterPin', methods=['POST'])
def enterPin():
    userid = request.form['userid']
    pin = int(request.form['pin'])

    if (pins[userid] != None):
        if (pins[userid][1] < time.time()):
            return 'Pin is not valid. please request a new one.'
        elif (pins[userid][0] != pin):
            return 'Pin invalid.'
        else: 
            pins[userid] = None
            return 'Access granted.'
    else:
        return 'No pin set, request a new pin.'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)