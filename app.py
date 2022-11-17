from flask import Flask
import os
from flaskr.extensions import db, migrate, login, admin
from flaskr.config import Config
import flaskr.blueprints.auth as auth
from flask_admin.contrib.sqla import ModelView
from flaskr.models import *
    
def register_extensions(app: Flask):
    """Register Flask extensions."""
    db.init_app(app) 
    migrate.init_app(app)
    login.init_app(app)
    login.login_view = 'login'
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Model, db.session))
    admin.add_view(ModelView(Feature, db.session))
    admin.add_view(ModelView(ModelType, db.session))
    return None
    
def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(auth.bp)
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