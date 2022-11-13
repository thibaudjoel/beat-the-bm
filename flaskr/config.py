from os import environ, path
from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = '570716b86a539094ae9f286094d3f45d3fefe2a3dcea2d48e3ba69b0e8af0640' #environ.get('SECRET_KEY')
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or \
        'sqlite:///' + path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False