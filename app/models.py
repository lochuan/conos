from . import db, jwt_st, jwt_lt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

users_boards = db.Table('users_boards',
                        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable = False),
                        db.Column('board_id', db.Integer, db.ForeignKey('boards.id'), nullable = False),
                        db.PrimaryKeyConstraint('user_id', 'board_id'))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Unicode(64), index = True)
    email = db.Column(db.String(64), unique = True)
    password_hash = db.Column(db.String(128))
    _confirmed = db.Column(db.SmallInteger, default = 0)
    thanks_received = db.Column(db.Integer, default = 0)
    boards = db.relationship('Board', secondary = users_boards, backref = db.backref('users', lazy = 'dynamic')) # Also create "users" in Board
    todos = db.relationship('Todo', backref = 'user')
    todos_ongoing = db.relationship('Todo_Ongoing', backref = 'user')
    todos_done = db.relationship('Todo_Done', backref = 'user')
    memos = db.relationship('Memo', backref = 'user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property 
    def confirmed(self):
        return self._confirmed

    @confirmed.setter
    def confirmed(self, value):
        self._confirmed = value
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def generate_auth_token(self):
        auth_token = jwt_lt.dumps({'user_id': self.id, 'user_name': self.name, 'user_email': self.email})
        auth_token = auth_token.decode('utf-8')
        return auth_token
        
    def generate_confirmed_token(self):
        confirmed_token = jwt_st.dumps({'email':self.email})
        confirmed_token = confirmed_token.decode('utf-8')
        return confirmed_token
    
        
    def __repr__(self):
        return '<User %r>' % self.username      

        
class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Unicode(64))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    todos = db.relationship('Todo', backref = 'board')
    todos_ongoing = db.relationship('Todo_Ongoing', backref = 'board')
    todos_done = db.relationship('Todo_Done', backref = 'board')
    memos = db.relationship('Memo', backref = 'board')
    
    def __repr__(self):
        return '<Role %r>' % self.name



class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.Unicode(128))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return 

class Todo_Ongoing(db.Model):
    __tablename__ = 'todos_ongoing'
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.Unicode(128))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return 

class Todo_Done(db.Model):
    __tablename__ = 'todos_done'
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.Unicode(128))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return 

class Memo(db.Model):
    __tablename__ = 'memos'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Unicode(128))
    content = db.Column(db.UnicodeText)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
