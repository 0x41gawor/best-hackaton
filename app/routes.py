from flask import render_template, url_for, redirect
from app import app, login
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from .models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


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

