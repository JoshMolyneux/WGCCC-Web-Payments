from flask import Flask, redirect, url_for, session, flash
from functools import wraps
import pymysql
from dotenv import load_dotenv
import os

project_folder = os.path.expanduser('www')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            flash("You are not logged in!", category='error')
            return redirect(url_for('auth.login'))
    return wrap


def sql_connect(host, port, user, password, database):
    connect = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    return connect


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    # will be set dependent on where the app is hosted

    from.views import views
    from.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
