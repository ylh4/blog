from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SeCrEt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dqrguzvhckgtvm:b5f28eb9809eac23b1f183b4be7a5a43257880d000e9f9525111007bcc3cb6ba@ec2-54-225-190-241.compute-'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
