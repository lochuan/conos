from flask import Flask
from itsdangerous import TimedJSONWebSignatureSerializer as JWT
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)
jwt_st = JWT(app.config['SECRET_KEY'], expires_in=3600, algorithm_name='HS256')
jwt_lt = JWT(app.config['SECRET_KEY'], expires_in=604800, algorithm_name='HS256')
auth = HTTPTokenAuth('Bearer')

from .views.user import user
from .views.board import board
from .views.todo import todo
from .views.member import member
from .views.memo import memo
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(board, url_prefix='/board')
app.register_blueprint(member, url_prefix='/member')
app.register_blueprint(todo, url_prefix='/todo')
app.register_blueprint(memo, url_prefix='/memo')