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
    THEN check the correct number of feature values
    """
    assert len(model_fulltime_goals.features[0].retrieve_values(model_fulltime_goals, [matches_scheduled[0]])) == 2
    assert len(model_fulltime_goals.features[0].retrieve_values(model_halftime_goals, [matches_scheduled[0]])) == 2
    
def test_