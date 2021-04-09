from flask import Flask
from flask import render_template, url_for, redirect
from flask_login import LoginManager, current_user, login_user, logout_user
from config import Config
from app.forms import LoginForm
from app.models import User


import json
import requests as r

app = Flask(__name__)
app.config.from_object(Config)
app.config["DEBUG"] = True
login = LoginManager(app)

@app.route('/')
def index():
    return "Test"

@login.user_loader
def load_user(id):
    user = User(4)
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        #send request to API (email, psswd)
        user = User(4)
        if user is None or not "form.password.data == database.password":
            #inform the user
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/<id>')
def main(id):
    data = json.loads(r.get('http://localhost:3000/home/{}'.format(id)).text)
    print(data)
    return render_template('main.html', data=data)

if __name__ == "__main__":
    app.run()