from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Placeholder user credentials (replace with secure storage)
users = {'admin': 'admin'}

@app.route('/', methods=['GET', 'POST'])
def main():
    # Content of the main page (replace with actual content)
    return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            # Successful login (replace with redirection to protected area)
            return redirect('/')
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)