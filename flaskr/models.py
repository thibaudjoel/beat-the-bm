from .extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    models = db.relationship("Model", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

model_features = db.Table('model_features',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('feature_id', db.Integer, db.ForeignKey('feature.id'), primary_key=True)
)

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    modeltype_id = db.Column(db.Integer, db.ForeignKey("modeltype.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    number_of_last_games = db.Column(db.Integer, nullable=False)
    
    user = db.relationship("User", back_populates="models")
    modeltype = db.relationship("ModelType", back_populates="models")
    features = db.relationship("Feature", secondary=model_features, back_populates="models")
    
    def __repr__(self) -> str:
        return f'<Model: {self.name} >'
    
    # def get_last_matches(amount: int, team):
    # pass

    # def build_feature_value(feature,matches, team):
    
class ModelType(db.Model):
    __tablename__ = 'modeltype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    
    models = db.relationship("Model", back_populates="modeltype")
    
    def __repr__(self) -> str:
        return f'<Modeltype: {self.name} >'

class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    
    models = db.relationship("Model", secondary=model_features, back_populates="features")
    
    def __repr__(self) -> str:
        return f'<Feature: {self.name} >'

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey("season.id"), nullable=False)
    matchday = db.Column(db.Integer, nullable=False)
    match_date_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer)
    home_team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    #score_id = db.Column(db.Integer, db.ForeignKey("score.id"), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey("season.id"), nullable=False)
    
    # B365D = db.Column(db.Float)
    # B365H = db.Column(db.Float)
    # B365A = db.Column(db.Float)
    score = db.relationship("Score", back_populates="match")
    season = db.relationship("Season", back_populates="matches")
    home_team = db.relationship("Team", backref="matches_home", foreign_keys=[home_team_id])
    away_team = db.relationship("Team", backref="matches_away", foreign_keys=[away_team_id])

class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), nullable=False)
    
    country = db.relationship("Country", back_populates="leagues")
    seasons = db.relationship("Season", back_populates="league")

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey("league_id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    current_matchday = db.Column(db.Integer)
    winner_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey("league.id"), nullable=False)
    
    winner = db.relationship("Team", back_populates="seasons_won", overlaps = "teams,season")
    league = db.relationship("League", back_populates="seasons")
    matches = db.relationship("Match", back_populates="season")
    teams = db.relationship("Team", back_populates="seasons", overlaps = "winner,season")

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    tla = db.Column(db.String)

    seasons = db.relationship("Season", back_populates="teams")
    # matches_away = db.relationship("Match", backref="away_team")
    # matches_home =  db.relationship("Match", backref="home_team", foreign_keys=[id])
    seasons_won = db.relationship("Season", back_populates="winner")

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    code = db.Column(db.String, unique=True)
    leagues = db.relationship("League", back_populates="country")
    
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winner = db.Column(db.String)
    fulltime_goals_home = db.Column(db.Integer)
    fulltime_goals_away = db.Column(db.Integer)
    halftime_goals_home = db.Column(db.Integer)
    halftime_goals_away = db.Column(db.Integer)
    
    match_id = db.Column(db.Integer, db.ForeignKey("match.id"), nullable=False)
    match = db.relationship("Match", back_populates="score")