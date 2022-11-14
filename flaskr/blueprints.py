import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from flaskr.models import User

from .forms import LoginForm, RegistrationForm, AccountSettingsForm

bp = Blueprint('auth', __name__, template_folder='Templates')
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

@bp.route('/account-settings', methods=['GET', 'POST'])
def account_settings():
    user = current_user
    form = AccountSettingsForm()
    return render_template('account_settings.html', title='Account Settings', user=user, form=form)
