import json

from flask import Flask, jsonify, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

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


@app.route('/users', methods=['GET'])
def index():
    users = db.session.query(UserModel)
    result = [{'name': getattr(d, 'name')} for d in users]
    return jsonify(users=result)


@app.route('/users/<int:id>', methods=['GET'])
def get_name(id):
    user = db.session.query(UserModel).filter(UserModel.id == id)
    return user[0].name


# simple call from terminal " curl -i "Content-Type: App;ication/json" -X POST http://127.0.0.1:5000/sample "
@app.route('/search', methods=['POST'])
def add_user():
    user = db.session.query(UserModel).filter(UserModel.name.ilike('%Ana%'))
    #user = db.session.query(UserModel).filter(func.lower(UserModel.name) == func.lower('zoe Abramson'))
    result = [{'id': getattr(d,'id'),'name': getattr(d, 'name')} for d in user]
    return jsonify(users=result)



if __name__ == "__main__":
    app.run(debug=True)
