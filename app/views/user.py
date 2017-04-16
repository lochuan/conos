from .. import app, db, auth, jwt
from flask import request, jsonify, make_response, g, Blueprint
from ..models import User
from ..email import send_email

user = Blueprint('user', __name__)

@user.route('/register', methods=['POST'])
def register():
	g.user=None
	if not request.json or not 'email' and 'password' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'Name, Email, or Password is missed'
			}
		return make_response(jsonify(responseObject)), 400
	g.user = User.query.filter_by(email=request.json['email']).first()
	if not g.user:
		try:
			g.user = User(name=request.json['username'], email=request.json['email'], password=request.json['password'])
			confirm_token = g.user.generate_confirmed_token()
			#send_email(g.user.email, 'Confirm Your Conos Account', 'confirm', user=g.user, token=confirm_token)
			auth_token = g.user.generate_auth_token()
			#db.session.add(g.user)
			#db.session.commit()
			responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered. Confirm mail sent',
                    'token': auth_token
                }
			return make_response(jsonify(responseObject)), 201
			
		except Exception as e:
			responseObject = {
						'status': 'fail',
						'message': 'Some error occurred. Please try again.',
						'error': str(e)
			}
			return make_response(jsonify(responseObject)), 401
	else:
		responseObject = {
				'status': 'fail',
				'message': 'User already exists. Please Log in.',
		}
		return make_response(jsonify(responseObject)), 202

		
@user.route('/get_token', methods=['POST'])
def login():
    if not request.json or not 'email' and 'password' in request.json:
        responseObject = {
                'status': 'fail',
                'message': 'Email, or Password is missed'
            }
        return make_response(jsonify(responseObject)), 400
    g.user=None
    g.user = User.query.filter_by(email=request.json['email']).first()
    if g.user == None:
            responseObject = {
                'status': 'fail',
                'message': 'No such Email'
            }
            return make_response(jsonify(responseObject)), 400
    else:
        if g.user.verify_password(request.json['password']):
            responseObject = {
                'status': 'success',
                'message': 'Successfully generate the token',
                'token': g.user.generate_auth_token()
            }
            return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Wrong password',
            }
            return make_response(jsonify(responseObject)), 400
              
@user.route('/confirm/<token>', methods=['GET'])
def confirm():
	pass
	
@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = jwt.loads(token)
    except:
        return False
    if 'user_email' and 'user_name' and 'user_id' in data:
        g.user = data['user_id']
        return True
    return False

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % g.user
