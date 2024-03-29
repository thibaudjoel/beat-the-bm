from .models import *
from .extensions import db

Feature()

from typing import List, Union


def query_all(classname: db.Model) -> List[db.Model]:
    return classname.query.all()


def query_all_features() -> List[Feature]:
    return Feature.query.all()


def query_all_modeltypes() -> List[ModelType]:
    return ModelType.query.all()


def query_all_matches() -> List[Match]:
    return Match.query.all()


def query_all_teams() -> List[Team]:
    return Team.query.all()


def query_all_countries() -> List[Country]:
    return Country.query.all()


def query_all_leagues() -> List[League]:
    return League.query.all()


def query_all_scores() -> List[Score]:
    return Score.query.all()


def query_all_users() -> List[User]:
    return User.query.all()


def query_all_models() -> List[Model]:
    return Model.query.all()


def query_all_seasons() -> List[Season]:
    return Season.query.all()


def query_match_on_id(id: str) -> Union[Match, None]:
    return Match.query.filter_by(id=id).first()


def query_country_on_id(id: str) -> Union[Country, None]:
    return Country.query.filter_by(id=id).first()


def query_team_on_id(id: str) -> Union[Team, None]:
    return Team.query.filter_by(id=id).first()


def query_league_on_id(id: str) -> Union[League, None]:
    return League.query.filter_by(id=id).first()


def query_season_on_id(id: str) -> Union[Season, None]:
    return Season.query.filter_by(id=id).first()


def query_league_on_code(code: str) -> Union[League, None]:
    return League.query.filter_by(code=code).first()


def query_match_on_matchday(matchday: int) -> Match | None:
    return Match.query.filter_by(matchday=matchday).first()
