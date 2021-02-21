import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SeCrEt'
app.config['SQLALCHEMY_DATABASE_URL'] = 'postgres://dqrguzvhckgtvm:b5f28eb9809eac23b1f183b4be7a5a43257880d000e9f9525111007bcc3cb6ba@ec2-54-225-190-241.compute-1.amazonaws.com:5432/de83ak2vi4ha7g'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from flaskblog import routes
