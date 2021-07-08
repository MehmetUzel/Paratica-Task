from flask import Flask, jsonify

app = Flask(__name__)

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


@app.route('/')
def index():
    return "First experiments.."


@app.route('/sample', methods=['GET'])
def get():
    return jsonify({'Users': sampleData})


@app.route('/sample/<int:index>', methods=['GET'])
def get_name(index):
    return jsonify({'User': sampleData[index]})


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


if __name__ == "__main__":
    app.run(debug=True)
