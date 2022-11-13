class team():
    pass

class match:
    pass
    

def get_last_matches(amount: int, team):
    pass

def build_feature_value(feature,matches, team):
    
class user:
    def __init__(self) -> None:
        pass
    
class model:
    def __init__(self,id: int, creator: user):
        self._id = id
        self.creator = creator
        
    @number_of_last_games.setter
    def number_of_last_games(self, number):
        self.number_of_last_games = number
        
    @features.setter
    def features(self, features):
        self.features = features
        
    @model_type.setter
    def model_type(self, value):
        self.model_type = model_type
        
    @title.setter
    def title(self, title):
        self.title = title
        
    def add_feature(self, feature):
        self.features.append(feature)
    
        
    


class prediction:
    def __init__(self, model: model, home_team: team, away_team: team, date):
        self.model = model
    
    def get_matches(self, team):
        amount = self.model.number_of_last_games
        
        
        
    pass