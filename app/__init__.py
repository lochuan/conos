from flask import Flask
from itsdangerous import TimedJSONWebSignatureSerializer as JWT
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)
jwt = JWT(app.config['SECRET_KEY'], expires_in=3600, algorithm_name='HS256')
auth = HTTPTokenAuth('Bearer')

from .views.user import user
from .views.board import board
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(board, url_prefix='/board')
