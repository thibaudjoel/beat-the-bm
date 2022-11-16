from .models import *
def all_features():
    return Feature.query.all()

def all_modeltypes():
    return ModelType.query.all()