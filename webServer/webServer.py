from flask import Flask, render_template, request, redirect, session, url_for, Response
from functools import wraps
import secrets
import random
import json
import mariadb

app = Flask(__name__)

config = {
    'host': 'db.tecnico.ulisboa.pt',
    'user': 'ist1110887',
    'password': 'rwhq1077',
    'database': 'ist1110887'
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
  data = {
    "temperature": "13C",
    "humidity": "20%",
    "luminosity": "Dark",
    "waterLeaks": "No leaks detected",
  }

  # Content of the main page (replace with actual content)
  return render_template('main.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)