from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, IntegerField, IntegerRangeField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError, InputRequired
from wtforms_sqlalchemy.orm import QuerySelectField, QuerySelectMultipleField

from .queries import query_all_features, query_all_modeltypes, query_all_seasons
from .models import User, Feature


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class FeatureForm(FlaskForm):
    featurename = StringField('Feature name', validators=[InputRequired()])
    submit = SubmitField('Save feature')
    
class ModelForm(FlaskForm):
    name = StringField('Model name', validators=[InputRequired()])
    number_of_last_games = IntegerField('Number of last games considered for prediction', validators=[InputRequired()])
    modeltype = QuerySelectField(query_factory=query_all_modeltypes, get_label='name', validators=[InputRequired()])
    features = QuerySelectMultipleField(query_factory=query_all_features, get_label='name', validators=[InputRequired()])
    seasons = QuerySelectMultipleField(query_factory=query_all_seasons, get_label='start_date', validators=[InputRequired()])
    submit = SubmitField('Save model')
    
class ModelTypeForm(FlaskForm):
    modeltype = StringField('Modeltype', validators=[InputRequired()])
    submit = SubmitField('Save model type')