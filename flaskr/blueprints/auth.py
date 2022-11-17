from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_user, logout_user

from app import db
from flaskr.models import User, Feature, Model, ModelType
from flask_login import login_required
from ..forms import LoginForm, RegistrationForm, FeatureForm, ModelForm, ModelTypeForm
from ..queries import *

bp = Blueprint('auth', __name__, template_folder='../Templates')
@bp.route('/')
@bp.route('/index')
def index():
    user = current_user
    return render_template('index.html', title='Home', user=user)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('auth.index'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/new_feature', methods=['GET', 'POST'])
@login_required
def features():
    form = FeatureForm()
    if form.validate_on_submit():
        feature = Feature.query.filter_by(name=form.featurename.data).first()
        if feature is not None:
            flash('Feature already exists')
        else: 
            feature = Feature(name=form.featurename.data)
            db.session.add(feature)
            db.session.commit()
            flash('Added new feature')
    return render_template('feature_create.html', title='New Feature', form=form)

@bp.route('/new_model', methods=['GET', 'POST'])
@login_required
def new_model():
    form = ModelForm()
    if form.validate_on_submit():
        model = Model.query.filter_by(name=form.name.data).first()
        if model is not None:
            flash('Name already exists')
        else:
            model = Model(user=current_user, modeltype=form.modeltype.data, name=form.name.data,
                          number_of_last_games=form.number_of_last_games.data, features=form.features.data)
            db.session.add(model)
            db.session.commit()
            flash('Added new model')
    else:
        flash('Wrong input')
    return render_template('model_create.html', title='New Model', form=form)

@bp.route('/new_modeltype', methods=['GET', 'POST'])
@login_required
def new_modeltype():
    form = ModelTypeForm()
    modeltype = ModelType.query.filter_by(name=form.modeltype.data).first()
    if modeltype is not None:
        flash('Modeltype already exists')
    else: 
        modeltype = ModelType(name=form.modeltype.data)
        db.session.add(modeltype)
        db.session.commit()
        flash('Added modeltype')
    return render_template('modeltype_create.html', title='New Modeltype', form=form)

@bp.route('/feature_overview', methods=['GET', 'POST'])
@login_required
def features_overview():
    query = all_features()
    attr_names = ['name', 'models']
    attr_lists = [[getattr(obj, attr_name) for attr_name in attr_names] for obj in query]
    return render_template('overview.html',attr_lists=attr_lists, attributes=attr_names, title='Feature Overview')

@bp.route('/user_overview', methods=['GET', 'POST'])
@login_required
def users_overview():
    query = all_users()
    attr_names = ['username', 'email', 'password_hash', 'models']
    attr_lists = [[getattr(obj, attr_name) for attr_name in attr_names] for obj in query]
    return render_template('overview.html',attr_lists=attr_lists, attributes=attr_names, title='User Overview')

@bp.route('/model_overview', methods=['GET', 'POST'])
@login_required
def model_overview():
    query = all_models()
    attr_names = ['name','number_of_last_games', 'user', 'modeltype', 'features']
    attr_lists = [[getattr(obj, attr_name) for attr_name in attr_names] for obj in query]
    return render_template('overview.html',attr_lists=attr_lists, attributes=attr_names, title='Model Overview')