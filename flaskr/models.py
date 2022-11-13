from .extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# class Model(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user_account.id"))
#     modeltype_id = db.Column(db.Integer, db.ForeignKey("modeltype.id"), nullable=False)
#     name = db.Column(db.String, nullable=False)
#     number_of_last_games = db.Column(db.Integer, nullable=False)
    
#     user_id = db.relationship("User", back_populates="models")
#     modeltype = db.relationship("ModelType", back_populates="models")
#     features = db.relationship("Feature", back_populates="models")
    
    # def get_last_matches(amount: int, team):
    # pass

    # def build_feature_value(feature,matches, team):
    
# class ModelType(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True)

# class Features(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True)

# class Match(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     season_id = db.Column(db.Integer, db.ForeignKey("season.id"), nullable=False)
#     match_date = db.Column(db.Date, nullable=False)
#     match_time = db.Column(db.Time, nullable=False)
#     home_team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
#     away_team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
#     full_time_home_team_goals = db.Column(db.Integer, nullable=False)
#     full_time_result = db.Column(db.Integer, nullable=False)
#     B365D = db.Column(db.Float)
#     B365H = db.Column(db.Float)
#     B365A = db.Column(db.Float)

#     season = db.relationship("Season", back_populates="matches")
#     home_team = db.relationship("Team", back_populates="matches")
#     away_team = db.relationship("Team", back_populates="matches")

# class League(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True)
#     country_id = db.Column(db.Integer, db.ForeignKey("country_id"), nullable=False)
    
#     country = db.relationship("Country", back_populates="leagues")
#     seasons = db.relationship("Season", back_populates="league")

# class Season(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     league_id = db.Column(db.Integer, db.ForeignKey("league_id"), nullable=False)
#     name = db.Column(db.String, nullable=False)
#     season_start = db.Column(db.Date, nullable=False)
#     season_end = db.Column(db.Date, nullable=False)
    
#     league = db.relationship("league", back_populates="seasons")
#     matches = db.relationship("Match", back_populates="seasons")

# # class Team(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String, unique=True, nullable=False)
# #     country_id = db.Column(db.Integer, db.ForeignKey("country_id"), nullable=False)

# #     country = db.relationship("Country", back_populates="teams")
# #     seasons = db.relationship("Season", back_populates="teams")
# #     matches = db.relationship("Match", back_populates="home_team", back_populates="away_team")

# class Country(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True)