from app import db
from .models import Feature, ModelType

def create_features(app):
    with app.app_context():
        names = ["fulltime_goals", "halftime_goals"]
        for name in names:
            if not Feature.query.filter_by(name=name).first():
                feature = Feature()
                feature.name = name
                db.session.add(feature)
            db.session.commit()
    
def create_modeltypes(app):
    with app.app_context():
        names = ['KNeighbors', 'DecisionTree', 'MLP', 'Ridge']
        for name in names:
            if not ModelType.query.filter_by(name=name).first():
                modeltype = ModelType()
                modeltype.name = name
                db.session.add(modeltype)
            db.session.commit()
