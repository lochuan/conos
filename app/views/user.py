from random import sample
from .. import app, db, auth, jwt
from flask import request, jsonify, make_response, g, Blueprint
from ..models import User
from ..email import send_email

user = Blueprint('user', __name__)

@user.route('/register/', methods=['POST'])
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
            auth_token = g.user.generate_auth_token()
            db.session.add(g.user)
            db.session.commit()
            confirm_token = g.user.generate_confirmed_token()
            send_email(g.user.email, 'Confirm Your Conos Account', 'confirm', user=g.user.name, token=confirm_token)
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
                        'error': str(e),
                        'info': request.json['username'],
                        'info2': request.json['email']
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

@user.route('/get_confirm_mail/', methods=['POST'])
def send_confirm_mail():
    g.user=None
    if not request.json or not 'email' in request.json:
        responseObject = {
                'status': 'fail',
                'message': 'Give an email address please.'
            }
        return make_response(jsonify(responseObject)), 400
    g.user = User.query.filter_by(email=request.json['email']).first()
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
    g.user = User.query.filter_by(email=request.json['email']).first()
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
            'message': 'Confirmation info is not a right type'
        }
        return make_response(jsonify(responseObject)), 400
            
@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = jwt.loads(token)
    except:
        return False
    if 'user_email' and 'user_name' and 'user_id' in data:
        g.user = User.query.filter_by(email=data['user_email']).first()
        return True
    return False
