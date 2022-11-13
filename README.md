# beat-the-bm

## Introduction
The project is intended to provide a web application that allows the end user to predict football match outcomes based on individually chosen data and algorithms.

## Technologies
The web app will be built using the flask framework in python.
### Libraries

flask_login: User Session Management (https://flask-login.readthedocs.io/en/latest/)  
flask_migrate: Database Migration (https://flask-migrate.readthedocs.io/en/latest/)  
flask_sqlalchemy: Object Relational Mapper (https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/, https://www.sqlalchemy.org/)    
WTForms: Forms Validation and Rendering (https://wtforms.readthedocs.io/en/3.0.x/).   

## Project directory
### App Configuration
The app configuration is handled in **`config.py`**
### Extensions
Extensions are managed in **`extensions.py`**
### Forms
Forms to handle user input are maintained in **`forms.py`**
### Models/Classes
Classes are maintained in **`models.py`**
### Blueprints
Blueprints to route from the url to an action or web page are handled in **`blueprints.py`**

## Further information
The match data is retrieved from https://www.football-data.org/.

## Launch
Launch is planned for mid december 2022.

## Project status
The project is currently still in the development stage.
