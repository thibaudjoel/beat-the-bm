from flask import Flask
import os
from flaskr.extensions import db, migrate, login
from flaskr.config import Config
import flaskr.blueprints as blueprints
    
def register_extensions(app: Flask):
    """Register Flask extensions."""
    db.init_app(app) 
    migrate.init_app(app)
    login.init_app(app)
    login.login_view = 'login'
    return None
    
def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(blueprints.bp)
    return None

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
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