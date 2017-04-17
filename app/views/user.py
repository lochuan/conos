import time
from random import sample
from .. import app, db, auth, jwt_lt
from flask import request, jsonify, make_response, g, Blueprint
from ..models import User
from ..email import send_email
from itsdangerous import TimedJSONWebSignatureSerializer as JWT_REFRESH


user = Blueprint('user', __name__)

@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = jwt_lt.loads(token, return_header=True)
    except:
        return False
    if 'user_email' and 'user_name' and 'user_id' in data[0]:
        g.user = User.query.filter_by(email=data[0]['user_email']).first()
        new_exp = int(data[1]['exp']) - int(time.time()) + 3600
        g.token = JWT_REFRESH(app.config['SECRET_KEY'], expires_in=new_exp, algorithm_name='HS256').dumps({'user_id': data[0]['user_id'], 'user_name': data[0]['user_name'], 'user_email': data[0]['user_email']})
        g.token = g.token.decode('utf-8')
        return True
    return False

@user.route('/register/', methods=['POST'])
def register():
    g.user=None
    if not request.json or not 'email' and 'password' in request.json:
        responseObject = {
                'status': 'fail',
                'message': 'Name, Email, or Password is missed'
            }
        return make_response(jsonify(responseObject)), 400
    try:
        g.user = User.query.filter_by(email=request.json['email']).first()
    except Exception as e:
        responseObject = {
                'status': 'fail',
                'message': 'database query error',
                'error': str(e)
        }
        return jsonify(responseObject), 500
    if not g.user:
        try:
            g.user = User(name=request.json['username'], email=request.json['email'], password=request.json['password'])
            auth_token = g.user.generate_auth_token()
            db.session.add(g.user)
            db.session.commit()
            #confirm_token = g.user.generate_confirmed_token()
            #send_email(g.user.email, 'Confirm Your Conos Account', 'confirm', user=g.user.name, token=confirm_token)
            responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered. Confirmation mail has been sent to %s' % g.user.email,
                    'token': auth_token
                }
            return make_response(jsonify(responseObject)), 201
            
        except Exception as e:
            responseObject = {
                        'status': 'fail',
                        'message': 'Some error occurred. Please try again.',                  
            }
            return make_response(jsonify(responseObject)), 401
        confirm_token = g.user.generate_confirmed_token()
        send_email(g.user.email, 'Confirm Your Conos Account', 'confirm', user=g.user.name, token=confirm_token)
    else:
        responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202

        
@user.route('/get_token/', methods=['POST'])
def send_token():
    if not request.json or not 'email' and 'password' in request.json:
        responseObject = {
                'status': 'fail',
                'message': 'Email, or Password is missed'
            }
        return make_response(jsonify(responseObject)), 400

    g.user=None

    try:
        g.user = User.query.filter_by(email=request.json['email']).first()
    except Exception as e:
        responseObject = {
                'status': 'fail',
                'message': 'database query error',
                'error': str(e)
        }
        return jsonify(responseObject), 500

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

@user.route('/get_confirm_mail/', methods=['POST'])
def send_confirm_mail():
    g.user=None
    if not request.json or not 'email' in request.json:
        responseObject = {
                'status': 'fail',
                'message': 'Give an email address please.'
            }
        return make_response(jsonify(responseObject)), 400
    try:
        g.user = User.query.filter_by(email=request.json['email']).first()
    except Exception as e:
        responseObject = {
                'status': 'fail',
                'message': 'database query error',
                'error': str(e)
        }
        return jsonify(responseObject), 500
    if g.user == None:
        responseObject = {
                'status': 'fail',
                'message': 'No such Email'
            }
        return make_response(jsonify(responseObject)), 400
    else:
        confirm_token = g.user.generate_confirmed_token()
        send_email(g.user.email, 'Confirm Your Conos Account', 'confirm', user=g.user.name, token=confirm_token)
        responseObject = {
                'status': 'success',
                'message': 'Confirmation mail has been sent to %s' % g.user.email
            }
        return make_response(jsonify(responseObject)), 200

@user.route('/forget_password/', methods=['POST'])
def send_new_password():
    g.user=None
    if not request.json or not 'email' in request.json:
        responseObject = {
                'status': 'fail',
                'message': 'Give an email address please.'
            }
        return make_response(jsonify(responseObject)), 400
    try:
        g.user = User.query.filter_by(email=request.json['email']).first()
    except Exception as e:
        responseObject = {
                'status': 'fail',
                'message': 'database query error',
                'error': str(e)
        }
        return jsonify(responseObject), 500
    if g.user == None:
        responseObject = {
                'status': 'fail',
                'message': 'No such Email'
            }
        return make_response(jsonify(responseObject)), 400
    else:
        new_password = ''.join(sample('0123456789', 6))
        g.user.password = new_password
        db.session.commit()
        send_email(g.user.email, 'Your New Conos Password', 'forget_password', user=g.user.name, password=new_password)
        responseObject = {
                'status': 'success',
                'message': 'New password has been sent to %s' % g.user.email
            }
        return make_response(jsonify(responseObject)), 200
             
@user.route('/confirm/<token>', methods=['GET'])
def confirm(token):
    g.user = None
    try:
        data = jwt.loads(token)
        if 'email' in data:
            g.user = User.query.filter_by(email=data['email']).first()
            g.user.confirmed = 1
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': '%s has been confirmed' % g.user.email
            }
            return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Confirm information can not match',
            }
            return make_response(jsonify(responseObject)), 400
    except Exception as e:
        responseObject = {
            'status': 'fail',
            'message': 'Confirmation link is wrong or expired'
        }
        return make_response(jsonify(responseObject)), 400
            