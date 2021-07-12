from flask import Flask, jsonify, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    # postgresql://postgres:{password}@localhost:{port}/{databasename}
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
def list_users():
    users = db.session.query(UserModel)
    result = [{'name': getattr(d, 'name')} for d in users]
    return jsonify(users=result)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_name(user_id):
    user = db.session.query(UserModel).filter(UserModel.id == user_id)
    return user[0].name


@app.route('/search', methods=['POST'])
def find_user():
    try:
        data = request.get_json()
        name = data['filter']['name']
        user = db.session.query(UserModel).filter(UserModel.name.ilike('%' + name + '%'))
    except KeyError:
        return "Please provide Json in correct format"
    except TypeError:
        return "Please provide a Json file"
    result = [{'id': getattr(d, 'id'), 'name': getattr(d, 'name')} for d in user]
    return jsonify(users=result)


@app.route('/save', methods=['PATCH'])
def save_user():
    try:
        data = request.get_json()

        userid = data['userId']
        action = data['action']
        timestamp = data['timestamp']
    except KeyError:
        return "Please provide Json in correct format"
    except TypeError:
        return "Please provide a Json file"

    useraction = UserAction(userid, action, timestamp)
    db.session.add(useraction)
    db.session.commit()
    return "success"


if __name__ == "__main__":
    app.run(debug=True)
