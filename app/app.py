from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def main():
    return render_template('main.html')