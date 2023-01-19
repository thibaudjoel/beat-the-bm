import pytest

from flaskr.models import User, ModelType, Feature, Match, Score, Season, Team, Model

@pytest.fixture(scope='module')
def new_user():
    user = User()
    user.username = 'test_username'
    user.email = 'test_email@test.com'
    user.set_password('test_password')
    return user

@pytest.fixture
def modeltype_kneighbors():
    modeltype = ModelType()
    modeltype.name = 'KNeighbors'
    return modeltype

@pytest.fixture
def modeltype_decisiontree():
    modeltype = ModelType()
    modeltype.name = 'DecisionTree'
    return modeltype

@pytest.fixture
def modeltype_mlp():
    modeltype = ModelType()
    modeltype.name = 'MLP'
    return modeltype

@pytest.fixture
def modeltype_ridge():
    modeltype = ModelType()
    modeltype.name = 'Ridge'
    return modeltype

@pytest.fixture
def modeltype_no_classifier():
    modeltype = ModelType()
    modeltype.name = 'NoClassifier'
    return modeltype

@pytest.fixture
def modeltype_wo_name():
    modeltype = ModelType()
    return modeltype
 
@pytest.fixture   
def feature_fulltime_goals():
    feature = Feature()
    feature.name = 'fulltime_goals'
    return feature

@pytest.fixture   
def feature_halftime_goals():
    feature = Feature()
    feature.name = 'halftime_goals'
    return feature

@pytest.fixture
def team_1():
    team = Team()
    team.name = 'team_1'
    return team

@pytest.fixture  
def team_2():
    team = Team()
    team.name = 'team_2'
    return team

@pytest.fixture
def team_3():
    team = Team()
    team.name = 'team_3'
    return team

@pytest.fixture
def score_1():
    score = Score()
    score.fulltime_goals_away = 3
    score.fulltime_goals_home = 2
    score.halftime_goals_away = 0
    score.halftime_goals_home = 1
    score.winner = 'AWAY_TEAM'
    return score

@pytest.fixture
def score_2():
    score = Score()
    score.fulltime_goals_away = 1
    score.fulltime_goals_home = 1
    score.halftime_goals_away = 1
    score.halftime_goals_home = 0
    score.winner = 'DRAW'
    return score

@pytest.fixture
def score_3():
    score = Score()
    score.fulltime_goals_away = 0
    score.fulltime_goals_home = 4
    score.halftime_goals_away = 0
    score.halftime_goals_home = 3
    score.winner = 'HOME_TEAM'
    return score

@pytest.fixture 
def matches_matchday_1(team_1, team_2, team_3, score_1, score_2, score_3):
    match_1 = Match()
    match_1.away_team = team_1
    match_1.home_team = team_2
    match_1.status = 'FINISHED'
    match_1.matchday = 1
    match_1.score = score_1
    
    match_2 = Match()
    match_2.away_team = team_1
    match_2.home_team = team_3
    match_2.status = 'FINISHED'
    match_2.matchday = 1
    match_2.score = score_2
    
    match_3 = Match()
    match_3.away_team = team_2
    match_3.home_team = team_3
    match_3.status = 'FINISHED'
    match_3.matchday = 1
    match_3.score = score_3
    
    return [match_1, match_2, match_3]
 
@pytest.fixture
def matches_matchday_2(team_1, team_2, team_3, score_1, score_2, score_3):
    match_1 = Match()
    match_1.away_team = team_1
    match_1.home_team = team_2
    match_1.status = 'FINISHED'
    match_1.matchday = 2
    match_1.score = score_2
    
    match_2 = Match()
    match_2.away_team = team_1
    match_2.home_team = team_3
    match_2.status = 'FINISHED'
    match_2.matchday = 2
    match_2.score = score_3
    
    match_3 = Match()
    match_3.away_team = team_2
    match_3.home_team = team_3
    match_3.status = 'FINISHED'
    match_3.matchday = 2
    match_3.score = score_1
    
    return [match_1, match_2, match_3]

@pytest.fixture 
def matches_matchday_3(team_1, team_2, team_3, score_1, score_2, score_3):
    match_1 = Match()
    match_1.away_team = team_1
    match_1.home_team = team_2
    match_1.status = 'FINISHED'
    match_1.matchday = 3
    match_1.score = score_3
    
    match_2 = Match()
    match_2.away_team = team_1
    match_2.home_team = team_3
    match_2.status = 'FINISHED'
    match_2.matchday = 3
    match_2.score = score_1
    
    match_3 = Match()
    match_3.away_team = team_2
    match_3.home_team = team_3
    match_3.status = 'FINISHED'
    match_3.matchday = 3
    match_3.score = score_2
    
    return [match_1, match_2, match_3]

@pytest.fixture
def matches_scheduled(team_1, team_2, team_3):
    match_1 = Match()
    match_1.away_team = team_1
    match_1.home_team = team_2
    match_1.status = 'SCHEDULED'
    match_1.matchday = 4
    
    match_2 = Match()
    match_2.away_team = team_1
    match_2.home_team = team_3
    match_2.status = 'SCHEDULED'
    match_2.matchday = 3
    
    match_3 = Match()
    match_3.away_team = team_2
    match_3.home_team = team_3
    match_3.status = 'SCHEDULED'
    match_3.matchday = 4
    
    return [match_1, match_2, match_3]


@pytest.fixture
def new_season(matches_matchday_1, matches_matchday_2, matches_matchday_3, matches_scheduled, team_1, team_2, team_3):
    season = Season()
    season.current_matchday = 4
    season.matches = [*matches_matchday_1, *matches_matchday_2, *matches_matchday_3, *matches_scheduled]
    season.teams = [team_1, team_2, team_3]
    return season

@pytest.fixture
def model_fulltime_goals(feature_fulltime_goals, modeltype_kneighbors, new_season):
    model = Model()
    model.features = [feature_fulltime_goals]
    model.modeltype = modeltype_kneighbors
    model.number_of_last_games = 1
    model.seasons = [new_season]

    return model

@pytest.fixture
def model_halftime_goals(feature_halftime_goals, new_season):
    model = Model()
    model.features = [feature_halftime_goals]
    model.number_of_last_games = 1
    model.seasons = [new_season]

    return model
