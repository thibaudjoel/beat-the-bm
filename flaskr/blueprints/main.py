from flask import Blueprint, jsonify

from flaskr.models import User, Feature, Model, ModelType
from ..queries import *

main = Blueprint("main", __name__)


@main.route("/add_model", methods=["POST"])
def add_model():

    return "Done", 201


@main.route("/add_feature", methods=["POST"])
def add_feature():

    return "Done", 201


@main.route("/models", methods=["GET"])
def models():
    models = query_all(Model)
    return jsonify({"models": models})


@main.route("/features", methods=["GET"])
def features():
    features = query_all(Feature)
    return jsonify({"features": features})


@main.route("/modeltypes", methods=["GET"])
def modeltypes():
    modeltypes = query_all(ModelType)
    return jsonify({"modeltypes": modeltypes})


@main.route("/matches", methods=["GET"])
def matches():
    matches = query_all(Match)
    return jsonify({"matches": matches})


@main.route("/seasons", methods=["GET"])
def seasons():
    seasons = query_all(Season)
    return jsonify({"seasons": seasons})


@main.route("/teams", methods=["GET"])
def teams():
    teams = query_all(Team)
    return jsonify({"teams": teams})


@main.route("/countries", methods=["GET"])
def countries():
    countries = query_all(Country)
    return jsonify({"countries": countries})


@main.route("/leagues", methods=["GET"])
def leagues():
    leagues = query_all(League)
    return jsonify({"leagues": leagues})


@main.route("/scores", methods=["GET"])
def scores():
    scores = query_all(Score)
    return jsonify({"scores": scores})
