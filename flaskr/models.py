from .extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from typing import List
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.base import ClassifierMixin as Classifier
from itertools import chain
import numpy as np
import pickle

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

model_features = db.Table('model_features',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id')),
    db.Column('feature_id', db.Integer, db.ForeignKey('feature.id'))
)

season_teams = db.Table('season_teams',
    db.Column('season_id', db.Integer, db.ForeignKey('season.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)
team_matches_home = db.Table('team_matches_home',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True)
)
team_matches_away = db.Table('team_matches_away',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True)
)

model_seasons = db.Table('model_seasons',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True),
    db.Column('season_id', db.Integer, db.ForeignKey('season.id'))
)

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    modeltype_id = db.Column(db.Integer, db.ForeignKey("modeltype.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    number_of_last_games = db.Column(db.Integer, nullable=False)
    classifier = db.Column(db.LargeBinary)
    
    #seasons used for training
    seasons = db.relationship("Season", secondary=model_seasons, back_populates="models")
    
    user = db.relationship("User", back_populates="models")
    
    #e.g. regression 
    modeltype = db.relationship("ModelType", back_populates="models")
    match_features = db.relationship("Feature", secondary=model_features, back_populates="models")
    
    def retrieve_feature_values(self, matches=None):
        if not matches:
            matches = list(chain(*[season.matches for season in self.seasons]))
        feature_values = []
        for feature in self.match_features:
            feature_values = feature.retrieve_values(self, matches)
        
        return feature_values
    
    def retrieve_targets(self):
        targets = []
        for match in chain(*[season.matches for season in self.seasons]):
            #make sure enough matches with match_features are available and match is played
            if match.matchday > self.number_of_last_games and match.status == 'FINISHED':
                targets.append(match.score.winner)
        return targets

    def train(self):
        targets = self.retrieve_targets()
        feature_values = self.retrieve_feature_values()
        classifier = self.modeltype.get_classifier()
        if classifier:
            self.classifier = pickle.dumps(classifier.fit(np.array(feature_values), targets))
            db.session.commit()
            
    def predict(self, match) -> str | None:
        if self.classifier:
            return pickle.loads(self.classifier).predict(np.array(self.retrieve_feature_values([match])))
        
    
    def __repr__(self) -> str:
        return f'<Model: {self.name} >'
    
class ModelType(db.Model):
    __tablename__ = 'modeltype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    
    models = db.relationship("Model", back_populates="modeltype")
    
    def get_classifier(self) -> Classifier | None:
        clf_dic = {
            'KNeighbors': KNeighborsClassifier(),
            'DecisionTree': DecisionTreeClassifier(),
            'MLP': MLPClassifier(),
            'Ridge': RidgeClassifier(),
            }
        classifier = clf_dic.get(self.name)
        
        return classifier
    
    def __repr__(self) -> str:
        return f'<Modeltype: {self.name} >'

class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    models = db.relationship("Model", secondary=model_features, back_populates="match_features")
    
    def retrieve_values(self, model, matches):
        #for each team for each game, get <number of last games> past feature values, return feature values and target value for the game
        feature_values = []
        if self.name == 'fulltime_goals' or self.name == 'halftime_goals':
            for match in matches:
                #make sure enough matches with match_features are available and that previous matches are already finished
                if match.matchday > model.number_of_last_games and match.matchday <= match.season.current_matchday + 1:
                    matchday = match.matchday
                    #get matches before the match according to number of matches to be used for the model
                    home_matches_home_team = filter(lambda match_: match.status == 'FINISHED' and match_.season == match.season and (matchday-model.number_of_last_games) <= match_.matchday < matchday, match.home_team.matches_home)
                    away_matches_home_team = filter(lambda match_: match.status == 'FINISHED' and match_.season == match.season and (matchday-model.number_of_last_games) <= match_.matchday < matchday, match.home_team.matches_away)
                    home_matches_away_team = filter(lambda match_: match.status == 'FINISHED' and match_.season == match.season and (matchday-model.number_of_last_games) <= match_.matchday < matchday, match.away_team.matches_home)
                    away_matches_away_team = filter(lambda match_: match.status == 'FINISHED' and match_.season == match.season and (matchday-model.number_of_last_games) <= match_.matchday < matchday, match.away_team.matches_away)
                    match_features = [None]*(model.number_of_last_games*2)
                    
                    #get match_features from matches sorted by matchdays, first for the home, then for the away team
                    if self.name == 'fulltime_goals':
                        for match in home_matches_home_team:
                            match_features[model.number_of_last_games-1+(matchday-match.matchday-1)] = match.score.fulltime_goals_home
                        for match in away_matches_home_team:
                            match_features[model.number_of_last_games-1+(matchday-match.matchday-1)] = match.score.fulltime_goals_away
                        for match in home_matches_away_team:
                            match_features[2*(model.number_of_last_games-1)+(matchday-match.matchday-1)] = match.score.fulltime_goals_home
                        for match in away_matches_away_team:
                            match_features[2*(model.number_of_last_games-1)+(matchday-match.matchday-1)] = match.score.fulltime_goals_away
                    
                    elif self.name == 'halftime_goals':
                        for match in home_matches_home_team:
                            match_features[model.number_of_last_games-1+(matchday-match.matchday-1)] = match.score.halftime_goals_home
                        for match in away_matches_home_team:
                            match_features[model.number_of_last_games-1+(matchday-match.matchday-1)] = match.score.halftime_goals_away
                        for match in home_matches_away_team:
                            match_features[2*(model.number_of_last_games-1)+(matchday-match.matchday-1)] = match.score.halftime_goals_home
                        for match in away_matches_away_team:
                            match_features[2*(model.number_of_last_games-1)+(matchday-match.matchday-1)] = match.score.halftime_goals_away
                feature_values.append(match_features)
        return feature_values
    
    def __repr__(self) -> str:
        return f'<Feature: {self.name} >'

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey("season.id"), nullable=False)
    matchday = db.Column(db.Integer, nullable=False)
    match_date_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer)
    score_id = db.Column(db.Integer, db.ForeignKey("score.id"), nullable=False)

    score = db.relationship("Score", back_populates="match")
    season = db.relationship("Season", back_populates="matches")
    away_team = db.relationship("Team", secondary=team_matches_away, back_populates="matches_away", uselist=False)
    home_team = db.relationship("Team", secondary=team_matches_home, back_populates="matches_home", uselist=False)

class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    code = db.Column(db.String, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), nullable=False)
    
    country = db.relationship("Country", back_populates="leagues")
    seasons = db.relationship("Season", back_populates="league")

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey("league_id"), nullable=False)
    name = db.Column(db.String, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    current_matchday = db.Column(db.Integer)
    winner_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    league_id = db.Column(db.Integer, db.ForeignKey("league.id"))
    teams = db.relationship("Team", secondary=season_teams, back_populates="seasons")
    winner = db.relationship("Team", back_populates="seasons_won")
    league = db.relationship("League", back_populates="seasons")
    matches = db.relationship("Match", back_populates="season")
    models = db.relationship("Model", secondary=model_seasons, back_populates="seasons")

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    tla = db.Column(db.String)

    seasons = db.relationship("Season", secondary=season_teams, back_populates="teams")
    matches_away = db.relationship("Match", secondary=team_matches_away, back_populates="away_team")
    matches_home = db.relationship("Match", secondary=team_matches_home, back_populates="home_team")
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
    
    match = db.relationship("Match", back_populates="score")