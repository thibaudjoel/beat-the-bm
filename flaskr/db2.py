from flask_sqlalchemy import SQLAlchemy

def init_db(app):
    db = SQLAlchemy(app)
    return db