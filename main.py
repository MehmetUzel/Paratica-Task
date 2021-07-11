import json

from flask import Flask, jsonify, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost:5432/paratica"
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<User {self.name}"


class UserAction(db.Model):
    __tablename__ = 'action'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    action = db.Column(db.String())
    timestamp = db.Column(db.DateTime())

    def __init__(self, user_id, action, timestamp):
        self.user_id = user_id
        self.action = action
        self.timestamp = timestamp


sampleData = [
    {
        "name": "Molecule Man",
        "index": 0,
        "age": 29,
        "secretIdentity": "Dan Jukes",
        "powers": [
            "Radiation resistance",
            "Turning tiny",
            "Radiation blast"
        ]
    },
    {
        "name": "Madame Uppercut",
        "age": 39,
        "index": 1,
        "secretIdentity": "Jane Wilson",
        "powers": [
            "Million tonne punch",
            "Damage resistance",
            "Superhuman reflexes"
        ]
    },
    {
        "name": "Eternal Flame",
        "age": 1000000,
        "index": 2,
        "secretIdentity": "Unknown",
        "powers": [
            "Immortality",
            "Heat Immunity",
            "Inferno",
            "Teleportation",
            "Interdimensional travel"
        ]
    }
]


@app.route('/users', methods=['GET'])
def index():
    users = db.session.query(UserModel)
    result = [{'name': getattr(d, 'name')} for d in users]
    return jsonify(users=result)


@app.route('/sample', methods=['GET'])
def get():
    return jsonify({'Users': sampleData})


@app.route('/users/<int:id>', methods=['GET'])
def get_name(id):
    user = db.session.query(UserModel).filter(UserModel.id == id)
    return user[0].name


# simple call from terminal " curl -i "Content-Type: App;ication/json" -X POST http://127.0.0.1:5000/sample "
@app.route('/sample', methods=['POST'])
def add_user():
    user = {
        "name": "Mehmet Uzel",
        "age": 999999999,
        "index": 3,
        "secretIdentity": "Ironman",
        "powers": [
            "Code Bending",
            "Writing code without bugs",
            "Googles like a god",
            "Mind Reading",
            "Best CS GO Player"
        ]
    }
    sampleData.append(user)
    return jsonify({'Created': sampleData})


# simple call from terminal " curl -i "Content-Type: App;ication/json" -X PUT http://127.0.0.1:5000/sample/0 "
@app.route("/sample/<int:index_change>", methods=['PUT'])
def user_update(index_change):
    sampleData[index_change]['secretIdentity'] = "Changed!"
    return jsonify({'user': sampleData[index_change]})


# simple call from terminal " curl -i "Content-Type: App;ication/json" -X DELETE http://127.0.0.1:5000/sample/0 "
@app.route("/sample/<int:index_delete>", methods=['DELETE'])
def user_delete(index_delete):
    sampleData.remove(sampleData[index_delete])
    return jsonify({'result': True})


if __name__ == "__main__":
    app.run(debug=True)
