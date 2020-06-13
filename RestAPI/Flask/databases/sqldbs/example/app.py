"""
Previously you have to install sqlite and configure it
"""
from flask import Flask, request, jsonify

# Do not forget to install these libraries in your virtualenv
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_URI = "sqlite:///" + os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Persons(db.Model):
    __tablename__ = "persons"

    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50))
    age = db.Column(db.String(3))

class personSchema(Schema):
    id = fields.Int()
    name = fields.Str()

@app.route("/")
def index():

    return "Hello World!"

@app.route("/api/persons/")
def get_all_persons():
    persons = Persons.query.all()
    person_schema = personSchema(many=True)
    results, errors = person_schema.dump(persons)

    return jsonify(results)

@app.route("/api/persons/<string:name>", methods=["GET"])
def get_one_person_by_name(name):
    person = Persons.query.filter_by(name=name).first()
    person_schema = personSchema()
    result, errors = person_schema.dump(person)

    return jsonify(result)

@app.route("/api/persons/", methods=["POST"])
def add_person():
    new_person = Persons(name=request.json["name"])
    db.session.add(new_person)
    db.session.commit()

    person_dict = {
            "id": new_person.id,
            "name": new_person.name,
            "age": new_person.age
            }

    return jsonify(person_dict)

@app.route("/api/persons/<int:id>", methods=["PUT"])
def edit_person(id):
    person = Persons.query.filter_by(id=id).first()
    person.name = request.json["name"]
    person.age = request.json["age"]

    db.session.commit()

    person_dict = dict(id=person.id, name=person.name, age=person.age)

    return jsonify(person_dict)

@app.route("/api/persons/<int:id>", methods=["DELETE"])
def delete_person(id):
    person = Persons.query.get(id)

    db.session.delete(person)
    db.session.commit()

    return jsonify({"message": "ok"})
