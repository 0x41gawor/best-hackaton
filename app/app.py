from flask import Flask
from flask import render_template, url_for, redirect, request
from flask_socketio import SocketIO, send
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models import User

import json
import requests as r

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "BETON-POLSKA-GUROM"
socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000")
login = LoginManager(app)

@login.user_loader
def load_user(id):
    user = User(id)
    return user

auth = {'data': [
    {
        'home_id': 561726292,
        'c_login': 'beton',
        'c_pass': 'bestssie'
    },
    {
        'home_id': 560912392,
        'c_login': 'beton2',
        'c_pass': 'bestssie2'
    },
]
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        login = request.form.get("login")
        password = request.form.get("password")

        for data in auth['data']:
            if login == data['c_login'] and password == data['c_pass']:
                home = data['home_id']
                user = User(home)
                login_user(user, remember=True)
                return redirect('/{}'.format(home))
        else:
            return redirect('/login')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@app.route('/')
def index():
    return redirect('/login')

@app.route('/<id>')
@login_required
def main(id):
    if current_user.id == id:
        data = json.loads(r.get('http://localhost:3000/home/{}'.format(id)).text)
        return render_template('main.html', data=data)
    else:
        return redirect('/{}'.format(current_user.id))

@app.errorhandler(401)
def page_not_found(e):
    return redirect('/login')

@socketio.on('connect_event')
def handle_connect_event(data):
    id = data['id']
    print("Connected from {}".format(id))

@socketio.on('message')
def handle_message(message):
    if message == "update":
        data = json.loads(r.get('http://localhost:3000/home/{}'.format(current_user.id)).text)
        send(data, json=True)

if __name__ == "__main__":
    socketio.run(app)