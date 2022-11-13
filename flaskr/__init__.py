import os
from flask import Flask, url_for, request, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    
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

    #@app.route("/")
    #def index():
    #    return render_template('../index.html')

    @app.route("/<string:name>")
    def page2(name):
        return f"Hi {name}"

    @app.route("/login", methods=['POST', 'GET'])
    def login():
        name = ""
        if request.method == 'POST':
            name = request.form['name']
        else:
            name = request.args.get('name')
        return f'Hi {name}'
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app

#if __name__ == '__main__':
 #   app = create_app()
  #  app.run(port=1617, debug=True)
