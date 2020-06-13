"""
Previously you have to install mongodb and create a schema with table
"""
from flask import Flask, jsonify, request
from flask_mongoalchemy import MongoAlchemy
from marshmallow import Schema, fields
# Do not forget to install the libraries in your virtualenv

app = Flask(__name__)

app.config["MONGOALCHEMY_DATABASE"] = "name_of_your_database"

db = MongoAlchemy(app)

class Person(db.Document): #YOU CAN CHANGE THIS CLASS NAME
    # You don't have to specify the ID row, it is created by default by mongo.
    # You can use the ID of the documents by "mongo_id" as a string.
    name = db.StringField()

class PersonSchema(Schema): #YOU CAN CHANGE THIS CLASS NAME
    # It takes the mongo_id attr and display it as "id".
    id = fields.Str(attribute="mongo_id")
    name = fields.Str()

@app.route("/")
def index():
    """
    This route is irrelevant for the REST API, you can delete it if you want to.
    """

    return "Hello World!"


# GET METHOD

@app.route("/api/persons/", methods=["GET"])
def get_persons():
    """
    This method uses the marshmallow library to serialize
    the persons objects and then serialize the result
    again to give a proper JSON response.

    You can use this method for the rest of the enpoints.
    """

    return jsonify(result)

@app.route("/api/persons/<string:name>")
def get_person_by_name(name):

    person_dict = {
        # This method to format a string only works in Python >= 3.6
        "id": f"{person.mongo_id}",
        "name": person.name
    }

    return jsonify(person_dict)


# POST METHOD

@app.route("/api/persons/", methods=["POST"])
def add_person():

    person_dict = {
        "id": "{}".format(new_person.mongo_id),
        "name": new_person.name
    }

    return jsonify(person_dict)


# PUT METHOD

@app.route("/api/persons/<string:id>", methods=["PUT"])
def edit_person(id):

    person_dict = {
        "id": "{}".format(person.mongo_id),
        "name": person.name
    }

    return jsonify(person_dict)


# DELETE METHOD

@app.route("/api/persons/<string:id>", methods=["DELETE"])
def delete_person(id):

    return jsonify({"message": "ok"})
