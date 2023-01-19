from app import db
from models import Feature

feature = Feature()
feature.name = 'fulltime_goals'
db.add(feature)
db.commit()