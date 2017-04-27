from . import db, jwt_st, jwt_lt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

users_boards = db.Table('users_boards',
                        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable = False),
                        db.Column('board_id', db.Integer, db.ForeignKey('boards.id'), nullable = False),
                        db.PrimaryKeyConstraint('user_id', 'board_id'))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64), index=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    _confirmed = db.Column(db.SmallInteger, default=0)
    thanks_received = db.Column(db.Integer, default=0)
    todos_created_num = db.Column(db.Integer, default=0)
    todos_done_num = db.Column(db.Integer, default=0)
    memos_created_num = db.Column(db.Integer, default=0)
    boards = db.relationship('Board', secondary=users_boards, backref=db.backref('users', lazy='dynamic')) # Also create "users" in Board
    todos = db.relationship('Todo', backref='user')
    todos_ongoing = db.relationship('Todo_Ongoing', backref='user')
    todos_done = db.relationship('Todo_Done', backref='user')
    memos = db.relationship('Memo', backref='user')
    thanks_to = db.relationship('Thanks', backref='user')
    meetup_times = db.relationship('Meetup_Times', backref = 'user', passive_deletes=True, lazy='dynamic')
    device_token = db.Column(db.String(128), default=None)

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
    
class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Unicode(64))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    todos = db.relationship('Todo', backref = 'board', passive_deletes=True)
    todos_ongoing = db.relationship('Todo_Ongoing', backref = 'board', passive_deletes=True)
    todos_done = db.relationship('Todo_Done', backref = 'board')
    memos = db.relationship('Memo', backref = 'board', passive_deletes=True)
    meetup_status = db.Column(db.SmallInteger, default=0)
    meetup_location = db.Column(db.Unicode(128), default=None)
    meetup_time = db.Column(db.DateTime, default=None)
    meetup_times = db.relationship('Meetup_Times', backref = 'board', passive_deletes=True, lazy='dynamic')
    
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.Unicode(128))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_changed_time = db.Column(db.DateTime, default=datetime.utcnow)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Todo_Ongoing(db.Model):
    __tablename__ = 'todos_ongoing'
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.Unicode(128))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Todo_Done(db.Model):
    __tablename__ = 'todos_done'
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.Unicode(128))
    thanks_received = db.Column(db.Integer, default = 0)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    thanks_from = db.relationship('Thanks', backref='todo_done')
    
class Memo(db.Model):
    __tablename__ = 'memos'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Unicode(128))
    content = db.Column(db.UnicodeText)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id', ondelete='CASCADE'))
    last_changed_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Thanks(db.Model):
    __tablename__ = 'thanks'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    done_id = db.Column(db.Integer, db.ForeignKey('todos_done.id'))

class Meetup_Times(db.Model):
    __tablename__ = 'meetup_times'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id', ondelete='CASCADE'))
    start_time = db.Column(db.DateTime, default=None)
    end_time = db.Column(db.DateTime, default=None)