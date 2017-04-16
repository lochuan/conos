from . import db, jwt
from werkzeug.security import generate_password_hash, check_password_hash


users_boards = db.Table('users_boards',
						db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable = False),
						db.Column('board_id', db.Integer, db.ForeignKey('boards.id'), nullable = False),
						db.PrimaryKeyConstraint('user_id', 'board_id'))

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique = True, index = True)
	email = db.Column(db.String(64), unique = True)
	password_hash = db.Column(db.String(128))
	confirmed = db.Column(db.Boolean, default = False)
	boards = db.relationship('Board', secondary = users_boards, backref = 'users') # Also create "users" in Board
	
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
		
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
		
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
		
	def generate_auth_token(self):
		auth_token = jwt.dumps({'user_id': self.id, 'user_name': self.name, 'user_email': self.email})
		auth_token = auth_token.decode('utf-8')
		return auth_token
		
	def generate_confirmed_token(self):
		confirmed_token = jwt.dumps({'id':self.id})
		confirmed_token = confirmed_token.decode('utf-8')
		return confirmed_token
	
	
		
	def __repr__(self):
		return '<User %r>' % self.username		

		
class Board(db.Model):
	__tablename__ = 'boards'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique = True)
	todos = db.relationship('Todo', backref = 'board')
	memos = db.relationship('Memo', backref = 'board')
	
	def __repr__(self):
		return '<Role %r>' % self.name



class Todo(db.Model):
	__tablename__ = 'todos'
	id = db.Column(db.Integer, primary_key = True)
	board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
	
	def __repr__(self):
		return 
		
class Memo(db.Model):
	__tablename__ = 'memos'
	id = db.Column(db.Integer, primary_key = True)
	board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
