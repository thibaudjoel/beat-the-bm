from flaskr.models import *

def test_user_password(new_user):
    """
    GIVEN a user
    WHEN a new user is created
    THEN check the email and password_hashed fields are defined correctly
    """
    assert new_user.password_hash != 'test_password'
    assert new_user.check_password('test_password')
    assert not new_user.check_password('TEST_PASSWORD')
    
def test_modeltypes(modeltype_kneighbors, modeltype_decisiontree, modeltype_mlp, modeltype_ridge, modeltype_no_classifier, modeltype_wo_name):
    """
    GIVEN a modeltype
    WHEN the classifier should be returned
    THEN check the correct classifier is returned
    """
    assert isinstance(modeltype_kneighbors.get_classifier(), KNeighborsClassifier)
    assert isinstance(modeltype_decisiontree.get_classifier(), DecisionTreeClassifier)
    assert isinstance(modeltype_mlp.get_classifier(), MLPClassifier)
    assert isinstance(modeltype_ridge.get_classifier(), RidgeClassifier)
    assert not modeltype_no_classifier.get_classifier()
    assert not modeltype_wo_name.get_classifier()
    
def test_features(model_fulltime_goals, model_halftime_goals, matches_scheduled):
    """
    GIVEN a feature
    WHEN the feature values are retrieved
    THEN check the twice the number of feature values matches
    the number of last games and the feature values are retrieved for all matches passed to the feature
    and do not contain None
    """
    assert len(model_fulltime_goals.features[0].retrieve_values(model_fulltime_goals, [matches_scheduled[0]])) == 1
    assert len(model_fulltime_goals.features[0].retrieve_values(model_halftime_goals, [matches_scheduled[0]])[0]) == 2*model_fulltime_goals.number_of_last_games
    assert not None in model_fulltime_goals.features[0].retrieve_values(model_fulltime_goals, [matches_scheduled[0]])
    assert len(model_fulltime_goals.features[0].retrieve_values(model_fulltime_goals, matches_scheduled[:2])) == 2
    assert len(model_fulltime_goals.features[0].retrieve_values(model_halftime_goals, matches_scheduled[:2])[0]) == 2*model_fulltime_goals.number_of_last_games
    assert not None in model_fulltime_goals.features[0].retrieve_values(model_fulltime_goals, matches_scheduled[:2])
    assert len(model_fulltime_goals.features[0].retrieve_values(model_fulltime_goals, matches_scheduled)) == 3
    assert len(model_fulltime_goals.features[0].retrieve_values(model_halftime_goals, matches_scheduled)[0]) == 2*model_fulltime_goals.number_of_last_games
    assert not None in model_fulltime_goals.features[0].retrieve_values(model_fulltime_goals, matches_scheduled)
    assert len(model_halftime_goals.features[0].retrieve_values(model_fulltime_goals, [matches_scheduled[0]])) == 1
    assert len(model_halftime_goals.features[0].retrieve_values(model_halftime_goals, [matches_scheduled[0]])[0]) == 2*model_halftime_goals.number_of_last_games
    assert not None in model_halftime_goals.features[0].retrieve_values(model_fulltime_goals, [matches_scheduled[0]])
    assert len(model_halftime_goals.features[0].retrieve_values(model_fulltime_goals, matches_scheduled[:2])) == 2
    assert len(model_halftime_goals.features[0].retrieve_values(model_halftime_goals, matches_scheduled[:2])[0]) == 2*model_halftime_goals.number_of_last_games
    assert not None in model_halftime_goals.features[0].retrieve_values(model_fulltime_goals, matches_scheduled[:2])
    assert len(model_halftime_goals.features[0].retrieve_values(model_fulltime_goals, matches_scheduled)) == 3
    assert len(model_halftime_goals.features[0].retrieve_values(model_halftime_goals, matches_scheduled)[0]) == 2*model_halftime_goals.number_of_last_games
    assert not None in model_halftime_goals.features[0].retrieve_values(model_fulltime_goals, matches_scheduled)
    
def test_model_kneighbors(model_fulltime_goals, model_halftime_goals, model_full_and_half_time_goals, matches_scheduled, modeltype_kneighbors):
    """
    GIVEN a model
    WHEN the model has features and modeltype of type kneighbors
    THEN check it can retrieve features and targets, be trained and after being trained predict matches
    """
    model_fulltime_goals.modeltype = modeltype_kneighbors
    model_halftime_goals.modeltype = modeltype_kneighbors
    model_full_and_half_time_goals.modeltype = modeltype_kneighbors
    model_fulltime_goals.train()
    model_halftime_goals.train()
    model_full_and_half_time_goals.train()
    assert len(model_fulltime_goals.retrieve_features()) == len(model_fulltime_goals.features)
    assert not None in model_fulltime_goals.retrieve_features()
    assert len(model_fulltime_goals.predict(matches_scheduled)) == len(matches_scheduled)
    assert model_fulltime_goals.classifier 
    assert model_fulltime_goals.predict(matches_scheduled)[0] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_fulltime_goals.predict(matches_scheduled)[1] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_fulltime_goals.predict(matches_scheduled)[2] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    
    assert len(model_halftime_goals.retrieve_features()) == len(model_halftime_goals.features)
    assert len(model_halftime_goals.predict(matches_scheduled)) == len(matches_scheduled)
    assert model_halftime_goals.classifier 
    assert model_halftime_goals.predict(matches_scheduled)[0] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_halftime_goals.predict(matches_scheduled)[1] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_halftime_goals.predict(matches_scheduled)[2] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    
    assert len(model_full_and_half_time_goals.retrieve_features()) == len(model_full_and_half_time_goals.features)
    assert len(model_full_and_half_time_goals.predict(matches_scheduled)) == len(matches_scheduled)
    assert model_full_and_half_time_goals.classifier 
    assert model_full_and_half_time_goals.predict(matches_scheduled)[0] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_full_and_half_time_goals.predict(matches_scheduled)[1] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_full_and_half_time_goals.predict(matches_scheduled)[2] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    
def test_model_decisiontree(model_fulltime_goals, model_halftime_goals, model_full_and_half_time_goals, matches_scheduled, modeltype_decisiontree):
    """
    GIVEN a model
    WHEN the model has features and modeltype of type decisiontree
    THEN check it can retrieve features and targets, be trained and after being trained predict matches
    """
    model_fulltime_goals.modeltype = modeltype_decisiontree
    model_halftime_goals.modeltype = modeltype_decisiontree
    model_full_and_half_time_goals.modeltype = modeltype_decisiontree
    model_fulltime_goals.train()
    model_halftime_goals.train()
    model_full_and_half_time_goals.train()
    assert len(model_fulltime_goals.retrieve_features()) == len(model_fulltime_goals.features)
    assert len(model_fulltime_goals.predict(matches_scheduled)) == len(matches_scheduled)
    assert model_fulltime_goals.classifier 
    assert model_fulltime_goals.predict(matches_scheduled)[0] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_fulltime_goals.predict(matches_scheduled)[1] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_fulltime_goals.predict(matches_scheduled)[2] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    
    assert len(model_halftime_goals.retrieve_features()) == len(model_halftime_goals.features)
    assert len(model_halftime_goals.predict(matches_scheduled)) == len(matches_scheduled)
    assert model_halftime_goals.classifier 
    assert model_halftime_goals.predict(matches_scheduled)[0] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_halftime_goals.predict(matches_scheduled)[1] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_halftime_goals.predict(matches_scheduled)[2] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    
    assert len(model_full_and_half_time_goals.retrieve_features()) == len(model_full_and_half_time_goals.features)
    assert len(model_full_and_half_time_goals.predict(matches_scheduled)) == len(matches_scheduled)
    assert model_full_and_half_time_goals.classifier 
    assert model_full_and_half_time_goals.predict(matches_scheduled)[0] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_full_and_half_time_goals.predict(matches_scheduled)[1] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_full_and_half_time_goals.predict(matches_scheduled)[2] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    
def test_model_mlp(model_fulltime_goals, model_halftime_goals, model_full_and_half_time_goals, matches_scheduled, modeltype_mlp):
    """
    GIVEN a model
    WHEN the model has features and modeltype of type mlp
    THEN check it can retrieve features and targets, be trained and after being trained predict matches
    """
    model_fulltime_goals.modeltype = modeltype_mlp
    model_halftime_goals.modeltype = modeltype_mlp
    model_full_and_half_time_goals.modeltype = modeltype_mlp
    model_fulltime_goals.train()
    model_halftime_goals.train()
    model_full_and_half_time_goals.train()
    assert len(model_fulltime_goals.retrieve_features()) == len(model_fulltime_goals.features)
    assert len(model_fulltime_goals.predict(matches_scheduled)) == len(matches_scheduled)
    assert model_fulltime_goals.classifier 
    assert model_fulltime_goals.predict(matches_scheduled)[0] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_fulltime_goals.predict(matches_scheduled)[1] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_fulltime_goals.predict(matches_scheduled)[2] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    
    assert len(model_halftime_goals.retrieve_features()) == len(model_halftime_goals.features)
    assert len(model_halftime_goals.predict(matches_scheduled)) == len(matches_scheduled)
    assert model_halftime_goals.classifier 
    assert model_halftime_goals.predict(matches_scheduled)[0] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_halftime_goals.predict(matches_scheduled)[1] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_halftime_goals.predict(matches_scheduled)[2] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    
    assert len(model_full_and_half_time_goals.retrieve_features()) == len(model_full_and_half_time_goals.features)
    assert len(model_full_and_half_time_goals.predict(matches_scheduled)) == len(matches_scheduled)
    assert model_full_and_half_time_goals.classifier 
    assert model_full_and_half_time_goals.predict(matches_scheduled)[0] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_full_and_half_time_goals.predict(matches_scheduled)[1] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_full_and_half_time_goals.predict(matches_scheduled)[2] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    
def test_model_ridge(model_fulltime_goals, model_halftime_goals, model_full_and_half_time_goals, matches_scheduled, modeltype_ridge):
    """
    GIVEN a model
    WHEN the model has features and modeltype of type ridge
    THEN check it can retrieve features and targets, be trained and after being trained predict matches
    """
    model_fulltime_goals.modeltype = modeltype_ridge
    model_halftime_goals.modeltype = modeltype_ridge
    model_full_and_half_time_goals.modeltype = modeltype_ridge
    model_fulltime_goals.train()
    model_halftime_goals.train()
    model_full_and_half_time_goals.train()
    assert len(model_fulltime_goals.retrieve_features()) == len(model_fulltime_goals.features)
    assert len(model_fulltime_goals.predict(matches_scheduled)) == len(matches_scheduled)
    assert model_fulltime_goals.classifier 
    assert model_fulltime_goals.predict(matches_scheduled)[0] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_fulltime_goals.predict(matches_scheduled)[1] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_fulltime_goals.predict(matches_scheduled)[2] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    
    assert len(model_halftime_goals.retrieve_features()) == len(model_halftime_goals.features)
    assert len(model_halftime_goals.predict(matches_scheduled)) == len(matches_scheduled)
    assert model_halftime_goals.classifier 
    assert model_halftime_goals.predict(matches_scheduled)[0] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_halftime_goals.predict(matches_scheduled)[1] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_halftime_goals.predict(matches_scheduled)[2] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    
    assert len(model_full_and_half_time_goals.retrieve_features()) == len(model_full_and_half_time_goals.features)
    assert len(model_full_and_half_time_goals.predict(matches_scheduled)) == len(matches_scheduled)
    assert model_full_and_half_time_goals.classifier 
    assert model_full_and_half_time_goals.predict(matches_scheduled)[0] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_full_and_half_time_goals.predict(matches_scheduled)[1] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    assert model_full_and_half_time_goals.predict(matches_scheduled)[2] in ['AWAY_TEAM', 'HOME_TEAM', 'DRAW']
    