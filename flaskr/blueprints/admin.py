from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_user, logout_user

from app import db
from flaskr.models import User, Feature, Model, ModelType
from flask_login import login_required
from ..forms import LoginForm, RegistrationForm, FeatureForm, ModelForm, ModelTypeForm
from ..queries import *

# bp = Blueprint('admin', __name__, template_folder='../Templates')
# @bp.route('/admin')
# def admin():
#     logout_user()
#     return redirect(url_for('admin.admin'))