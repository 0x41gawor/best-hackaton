from flask import Flask
from flask import render_template, url_for, redirect, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from config import Config
from forms import LoginForm
from models import User

import json
import requests as r

app = Flask(__name__)
app.config.from_object(Config)
app.config["DEBUG"] = True
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

if __name__ == "__main__":
    app.run()