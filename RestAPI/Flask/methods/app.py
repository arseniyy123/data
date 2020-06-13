from flask import Flask, jsonify, request

app = Flask(__name__)

persons = [
        {
            "id": 1,
            "name": "Alice",
            "age": "21"
            },
        {
            "id": 2,
            "name": "Peter",
            "age": "17"
            },
        {
            "id": 3,
            "name": "Jorge",
            "age": "23"
            },
        {
            "id": 4,
            "name": "Clara",
            "age": "24"
            },
        {
            "id": 5,
            "name": "Tomas",
            "age": "25"
            }
        ]

# This route is irrelevant for the REST API, you can delete it if you wish.
@app.route("/")
def index():

    return "Hello World!"


# GET METHOD

@app.route("/api/persons/", methods=["GET"])
def get_persons():

    return jsonify(persons)

@app.route("/api/persons/<string:name>")
def get_person_by_name(name):
    person = []
    for f in person:
        if f["name"] == name:
            person.append(f)

    return jsonify(person[0])


# POST METHOD

@app.route("/api/persons/", methods=["POST"])
def add_person():
    person = {
            "id": request.json["id"],
            "name": request.json["name"],
            "age": request.json["age"]
            }
    persons.append(person)

    return jsonify(person)


# PUT METHOD

@app.route("/api/persons/<int:id>", methods=["PUT"])
def edit_person(id):
    person = [person for person in persons if person["id"] == id]

    person = person[0]
    person["id"] = request.json["id"]
    person["name"] = request.json["name"]

    return jsonify(person)


# DELETE METHOD

@app.route("/api/persons/<int:id>", methods=["DELETE"])
def delete_person(id):
    person = [person for person in persons if person["id"] == id]

    persons.remove(person[0])

    return jsonify({"message": "ok"})

if __name__ == "__main__":
    # Debug mode is only for development mode, you can turn it off
    app.run(debug=True)
