from app import db
from models import Feature

feature = Feature()
feature.name = 'goals_scored'
db.add(feature)
db.commit()