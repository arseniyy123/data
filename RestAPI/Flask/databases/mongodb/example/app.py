'''
Previously you have to install mongodb and create a schema with table persons
'''

from flask import Flask, jsonify, request
from flask_mongoalchemy import MongoAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config["MONGOALCHEMY_DATABASE"] = "persons"
db = MongoAlchemy(app)

class Person(db.Document):
    name = db.StringField()

class PersonSchema(Schema):
    id = fields.Str(attribute="mongo_id")
    name = fields.Str()

@app.route("/")
def index():

    return "Hello World!"


# GET METHOD

@app.route("/api/persons/", methods=["GET"])
def get_persons():
    persons = Person.query.all()
    persons_schema = PersonSchema(many=True)
    results, errors = persons_schema.dump(persons)

    return jsonify(results)

@app.route("/api/persons/<string:name>")
def get_person_by_name(name):
    person = Person.query.filter(Person.name == name).first()
    person_schema = PersonSchema()
    result = person_schema.dump(person)

    return jsonify(result)


# POST METHOD

@app.route("/api/persons/", methods=["POST"])
def add_person():
    new_person = Person(name=request.json["name"])
    new_person.save()

    person_dict = {
        "id": "{}".format(new_person.mongo_id),
        "name": new_person.name,
        "age": new_person.age
    }

    return jsonify(person_dict)


# PUT METHOD

@app.route("/api/persons/<string:id>", methods=["PUT"])
def edit_person(id):
    person = Person.query.get(id)
    person.name = request.json["name"]
    person.age = request.json["age"]

    person_dict = {
        # This method to format a string only works in Python >= 3.6
        "id": f"{person.mongo_id}",
        "name": person.name,
        "age": person.age
    }

    return jsonify(person_dict)


# DELETE METHOD

@app.route("/api/persons/<string:id>", methods=["DELETE"])
def delete_person(id):
    person = Person.query.get(id)
    person.remove()

    return jsonify({"message": "ok"})