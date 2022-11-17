from .models import *
def all_features():
    return Feature.query.all()

def all_modeltypes():
    return ModelType.query.all()

def all_users():
    return User.query.all()

def all_models():
    return Model.query.all()