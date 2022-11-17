from .models import *
def query_all_features()->list[Feature]:
    return Feature.query.all()

def query_all_modeltypes()->list[ModelType]:
    return ModelType.query.all()

def query_all_users()->list[User]:
    return User.query.all()

def query_all_models()->list[Model]:
    return Model.query.all()

def query_match_on_id(id)->Match or None:
    return Match.query.filter_by(id=id).first()

def query_country_on_id(id)->Country or None:
    return Match.query.filter_by(id=id).first()

def query_team_on_id(id)->Team or None:
    return Match.query.filter_by(id=id).first()

def query_league_on_id(id)->League or None:
    return Match.query.filter_by(id=id).first()

def query_season_on_id(id)->Season or None:
    return Match.query.filter_by(id=id).first()