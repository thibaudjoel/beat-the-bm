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
    return jsonify({"models": list(map(lambda x: x.to_json(), models))})


@main.route("/features", methods=["GET"])
def features():
    features = query_all(Feature)
    return jsonify({"features": list(map(lambda x: x.to_json(),features))})


@main.route("/modeltypes", methods=["GET"])
def modeltypes():
    modeltypes = query_all(ModelType)
    return jsonify({"modeltypes": list(map(lambda x: x.to_json(), modeltypes))})


@main.route("/matches", methods=["GET"])
def matches():
    matches = query_all(Match)
    return jsonify({"matches": list(map(lambda x: x.to_json(),matches))})


@main.route("/seasons", methods=["GET"])
def seasons():
    seasons = query_all(Season)
    return jsonify({"seasons": list(map(lambda x: x.to_json(),seasons))})


@main.route("/teams", methods=["GET"])
def teams():
    teams = query_all(Team)
    return jsonify({"teams": list(map(lambda x: x.to_json(),teams))})


@main.route("/countries", methods=["GET"])
def countries():
    countries = query_all(Country)
    return jsonify({"countries": list(map(lambda x: x.to_json(),countries))})


@main.route("/leagues", methods=["GET"])
def leagues():
    leagues = query_all(League)
    return jsonify({"leagues": list(map(lambda x: x.to_json(),leagues))})


@main.route("/scores", methods=["GET"])
def scores():
    scores = query_all(Score)
    return jsonify({"scores": list(map(lambda x: x.to_json(), scores))})
