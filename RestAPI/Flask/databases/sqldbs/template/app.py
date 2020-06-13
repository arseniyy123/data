"""
Previously you have to install sqlite and configure it
"""
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

import os

# This method gets an absolute path of a file; works with all the operative systems.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
"""
If you're using MySQL or PostegreSQL you'll need to use another connector. Check in Google how to deal with it
"""
DB_URI = "sqlite:///" + os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Persons(db.Model):
    __tablename__ = "persons"

    # The id will be unique, cannot be null, and auto-increase.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.String(3))


# This route is irrelevant for the REST API, you can delete it if you want to.
@app.route("/")
def index():
    return "Hello World!"


# GET METHOD

@app.route("/api/persons/", methods=["GET"])
def get_persons():
    return jsonify(persons)


@app.route("/api/persons/<string:name>")
def get_person_by_name(name):
    return jsonify(person)


# POST METHOD

@app.route("/api/persons/", methods=["POST"])
def add_person():
    return jsonify(person)


# PUT METHOD

@app.route("/api/persons/<int:id>", methods=["PUT"])
def edit_person(id):
    return jsonify(person)


# DELETE METHOD

@app.route("/api/persons/<int:id>", methods=["DELETE"])
def delete_person(id):
    return jsonify({"message": "ok"})

