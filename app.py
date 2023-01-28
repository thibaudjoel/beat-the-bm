from flask import Flask
from flask_admin.contrib.sqla import ModelView

import os

from flaskr.config import Config
from flaskr.extensions import db, migrate, login, admin
from flaskr.models import *

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
def register_extensions(app: Flask):
    """Register Flask extensions."""
    db.init_app(app, ) 
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'login'
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Model, db.session))
    admin.add_view(ModelView(Feature, db.session))
    admin.add_view(ModelView(ModelType, db.session))
    admin.add_view(ModelView(Match, db.session))
    admin.add_view(ModelView(Team, db.session))
    admin.add_view(ModelView(Score, db.session))
    admin.add_view(ModelView(Country, db.session))
    admin.add_view(ModelView(Season, db.session))
    admin.add_view(ModelView(League, db.session))
    
    return None
    
def register_blueprints(app):
    """Register Flask blueprints."""
    from flaskr.blueprints import admin, auth, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.main)
    return None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    register_extensions(app)
    register_blueprints(app)
    @app.before_first_request
    def create_tables():
        db.create_all()
    return app

app = create_app()