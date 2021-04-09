from flask import Flask
from flask import render_template

import json
import requests as r

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/<id>')
def main(id):
    data = json.loads(r.get('http://localhost:3000/home/{}'.format(id)).text)
    print(data)
    return render_template('main.html', data=data)

if __name__ == "__main__":
    app.run()