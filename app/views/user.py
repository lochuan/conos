import time
from random import sample
from .. import app, db, auth, jwt_lt, jwt_st
from flask import request, jsonify, make_response, g, Blueprint
from ..models import User, Todo, Todo_Ongoing, Todo_Done, Board, Thanks
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
            confirm_token = g.user.generate_confirmed_token()
            send_email(g.user.email, 'Confirm Your Conos Account', 'confirm', user=g.user.name, token=confirm_token)
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

@user.route('/change_password/', methods=['POST'])
def change_password():
    if not request.json or not 'email' in request.json or not 'old_password' in request.json or not 'new_password' in request.json:
        responseObject = {
                'status': 'fail',
                'message': 'Wrong data received'
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
        if g.user.verify_password(request.json['old_password']):
            g.user.password = request.json['new_password']
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Password has changed successfully',
                'token': g.user.generate_auth_token()
            }
            return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Old password does not match',
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
    elif g.user.confirmed == 0:
        responseObject = {
                'status': 'fail',
                'message': 'Your email have not confirmed yet, Please confirm your email first'
        }
        return jsonify(responseObject), 400
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
        data = jwt_st.loads(token)
        if 'email' in data:
            g.user = User.query.filter_by(email=data['email']).first()
            g.user.confirmed = 1
            db.session.commit()
            return make_response("<h2>Your email: %s has been confirmed!</h2>" % g.user.email), 200
        else:
            return make_response("<h2>Confirmation Info Error</h2>"), 400
    except Exception as e:
        return make_response("<h2>Confimation link is wrong or expired</h2>"), 400
            

@user.route('/', methods=['GET'])
@auth.login_required
def send_user_profile():
    todo_list = []
    todo_ongoing_list = []
    thanks_from_list = []
    board_list = []
    todo_done_list = []
    for todo in g.user.todos:
        if todo.board_id == None:
            db.session.delete(todo)
            continue
        todo_info = {
            'todo_id':todo.id,
            'todo_item': todo.item,
            'in_board': todo.board_id,
            'todo_last_changed_time': todo.last_changed_time
        }
        todo_list.append(todo_info)
    for todo_ongoing in g.user.todos_ongoing:
        if todo_ongoing.board_id == None:
            db.session.delete(todo_ongoing)
            continue
        todo_ongoing_info = {
            'todo_ongoing_id': todo_ongoing.id,
            'todo_ongoing_item': todo_ongoing.item,
            'in_board': todo_ongoing.board_id

        }
        todo_ongoing_list.append(todo_ongoing_info)
    for todo_done in g.user.todos_done:
        todo_done_info = {
            'todo_done_id': todo_done.id,
            'todo_done_item': todo_done.item,
        }
        todo_done_list.append(todo_done_info)
    for board in g.user.boards:
        board_info = {
            'board_id': board.id,
            'board_name': board.name
        }
        board_list.append(board_info)
    db.session.commit()
    return jsonify({"thanks_received": g.user.thanks_received, "todo":todo_list, "todos_ongoing": todo_ongoing_list, "todos_done":todo_done_list}), 200