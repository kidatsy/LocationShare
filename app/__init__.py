from flask import Flask
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
import flask.ext.login as flask_login
import os

username,password = "eric_schles","1234"
app = Flask(__name__)
#if on localhost: app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://"+username+":"+password+"@localhost/location_share"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.secret_key = 'super secret string'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

from app import views,models
