from flask import Flask, render_template, request, redirect, session, url_for, Response
from functools import wraps
import secrets
import random
import json
import mariadb
import plotly.graph_objs as go
import os

import time
from datetime import datetime

app = Flask(__name__)

config = {
    'host': os.environ['DB_HOST'],
    'user': os.environ['DB_USERNAME'],
    'password': os.environ['DB_PASSWORD'],
    'database': os.environ['DB_NAME']
}

conn = mariadb.connect(**config)
cur = conn.cursor()

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
@login_required
def analytics():
    # replace with database retrieval
    humidity_values = [30, 35, 40, 60, 70, 40, 20]
    temperature_values = [30, 32, 36, 40, 38, 36, 35]
    timestamps = [
        datetime(2024, 3, 8, 9, 0),  # 9:00 AM
        datetime(2024, 3, 8, 10, 0),  # 10:00 AM
        datetime(2024, 3, 8, 11, 0),  # 11:00 AM
        datetime(2024, 3, 8, 12, 0),  # 12:00 PM
        datetime(2024, 3, 8, 13, 0),  # 1:00 PM
        datetime(2024, 3, 8, 14, 0),  # 2:00 PM
        datetime(2024, 3, 8, 15, 0),  # 3:00 PM
    ]

    # Create temperature graph
    trace = go.Scatter(x=timestamps, y=temperature_values, mode='lines+markers', name='Humidity')
    layout = go.Layout(title='Humidity Over Time',
                       xaxis=dict(title='Time'),
                       yaxis=dict(title='Humidity (%)'))
    fig = go.Figure(data=[trace], layout=layout)
    temperature_graph_json = fig.to_json()

    # Create humidity graph
    trace = go.Scatter(x=timestamps, y=humidity_values, mode='lines+markers', name='Humidity')
    layout = go.Layout(title='Humidity Over Time',
                       xaxis=dict(title='Time'),
                       yaxis=dict(title='Humidity (%)'))
    fig = go.Figure(data=[trace], layout=layout)
    humidity_graph_json = fig.to_json()

    return render_template('analytics.html', data={'humidity': humidity_graph_json, 'temperature': temperature_graph_json})

@app.route('/add_footage', methods=['POST'])
def add_footage():
    media = request.data

    filename = 'media-' + str(time.time()) + '.mp3'

    with open(filename, 'wb') as f:
        f.write(media)

    return 'Footage added'

@app.route('/add-measure', methods=['POST'])
def addMeasure():
  time = request.form['timestamp']
  value = request.form['value']
  sensorid = request.form['sensorid']
  print(time, value, sensorid)
  if not sensorid or not value or not time:
     return Response(status=400)
  
  sql= "INSERT INTO MEASUREMENTS (SENSORID, MEASURE_TIMESTAMP, VALUE) VALUES (?,?,?)"
  data= (sensorid, time, value)
  cur.execute(sql, data)

  conn.commit()

  return Response(status=200)

@app.route('/', methods=['GET', 'POST'])
@login_required
def main():
  #TODO fetch values from DB  
  # Qualify light
  light_value = 250
  if light_value < 50:
      light = 'dark'
  elif light_value < 500:
      light = 'dim'
  else:
      light = 'bright'

  data = {
    "temperature": 13,
    "humidity": 20,
    "luminosity": light,
    "waterLeaks": "No leaks detected",
  }

  # Content of the main page (replace with actual content)
  return render_template('main.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)