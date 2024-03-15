from flask import Flask, render_template, request, redirect, session, url_for, Response
from functools import wraps
import secrets
import json
import mariadb
import plotly.graph_objs as go
import cv2
import numpy as np
import time, datetime
import os, sys, random

app = Flask(__name__)

config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

pool = mariadb.ConnectionPool(
    pool_name='banana',
    pool_size=5,
    **config
)

# Placeholder user credentials (replace with secure storage)
users = {'user1': 'user1', 'user2': 'user2'}
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
            return redirect('/')
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/logout', methods=['POST'])
@login_required
def logout():    
    del session['logged_in']
    return redirect('/login')

@app.route('/getPin', methods=['POST'])
@login_required
def get_pin():
    # Generate a random integer between 1000 and 9999 (inclusive)
    pin = random.randint(1000, 9999)

    # TODO: Store the pin in the DB with the timestamp
    return render_template('getpin.html', pin=pin)

@app.route('/analytics', methods=['POST'])
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
                       yaxis=dict(title='Humidity (%)'))
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


@app.route('/add-measure', methods=['POST'])
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

@app.route('/add-footage', methods=['POST'])
def addFootage():
  # Receive the video file from the server
  videofile = request.files['video']
  videofile.save('./media/video_' + str(time.time()) + '.avi')

  return Response(status=200)

@app.route('/', methods=['GET'])
#@login_required
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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)