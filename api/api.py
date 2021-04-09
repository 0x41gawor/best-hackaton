import flask
from flask_restful import Api, abort, Resource
from datetime import datetime

from model import DATA

app = flask.Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

def abort_if_home_doesnt_exist(id):
    ids = []

    for home in DATA['homes']:
        ids.append(home['id'])

    if int(id) not in ids:
        abort(404, message="Home of id {} doesn't exist".format(id))

class Homes(Resource):
    def get(self):
        return DATA['homes']

class Home(Resource):
    def get(self, id):
        abort_if_home_doesnt_exist(int(id))
        for n, home in enumerate(DATA['homes']):
            if home['id'] == int(id):
                return home

api.add_resource(Homes, '/homes')
api.add_resource(Home, '/home/<id>')

if __name__ == "__main__":
    app.run(port=3000)
