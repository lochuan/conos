from random import sample
from .. import app, db, auth, jwt_lt, jwt_st
from flask import request, jsonify, make_response, g, Blueprint
from ..models import User, Todo, Todo_Ongoing, Todo_Done, Board, Thanks
from ..email import send_email


user = Blueprint('user', __name__)

@user.route('/register/', methods=['POST'])
def register():
    g.user=None
    repa = ('email', 'password', 'name')
    if not request.json or not all(para in repa for para in request.json):
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
            g.user = User(name=request.json['name'], email=request.json['email'], password=request.json['password'])
            auth_token = g.user.generate_auth_token()
            db.session.add(g.user)
            db.session.commit()
            confirm_token = g.user.generate_confirmed_token()
            send_email(g.user.email, 'Confirm Your Conos Account', 'confirm', user=g.user.name, token=confirm_token)
            responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered. Confirmation mail has been sent to (%s)' % g.user.email,
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
    repa = ('email', 'password')
    if not request.json or not all(para in repa for para in request.json):
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
    repa = ('email', 'old_password', 'new_password')
    if not request.json or not all(para in repa for para in request.json):
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
                'message': 'Password has been changed successfully',
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
                'message': 'Confirmation mail has been sent to (%s)' % g.user.email
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
                'message': 'New password has been sent to (%s)' % g.user.email
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
            return make_response("<h2>Your email: (%s) has been confirmed!</h2>" % g.user.email), 200
        else:
            return make_response("<h2>Confirmation Info Error</h2>"), 400
    except Exception as e:
        return make_response("<h2>Confimation link is wrong or expired</h2>"), 400

@user.route('/', methods=['PUT'])
@auth.login_required
def update_user_profile():
    repa = ('name','device_token')
    if not request.json or not all(para in repa for para in request.json):
        responseObject = {
                'status': 'fail',
                'message': 'You need to give name and device_token',
                'token': g.token
            }
        return make_response(jsonify(responseObject)), 400
    
    if request.json['name'] == 'null':
        pass
    else:
        g.user.name = request.json['name']
    if request.json['device_token'] == 'null':
        pass
    else:
        g.user.device_token = request.json['device_token']
    db.session.commit()
    responseObject = {
        'status': ' success',
        'message': 'user profile has been updated'
    }
    return jsonify(responseObject), 200

@user.route('/', methods=['GET'])
@auth.login_required
def send_user_profile():
    board_list = []
    thanks_to_list = []
    try:
        for board in g.user.boards:        
            todo_list = []
            todo_ongoing_list = []
            todo_done_list = []
            member_list = []
            memo_list = []
            for todo in board.todos:
                todo_info = {
                    'todo_id':todo.id,
                    'todo_item': todo.item,
                    'todo_last_changed_time': todo.last_changed_time,
                    'creator': todo.user.name
                }
                if todo_info in todo_list:
                    continue
                todo_list.append(todo_info)
            for todo_ongoing in board.todos_ongoing:
                todo_ongoing_info = {
                    'todo_ongoing_id': todo_ongoing.id,
                    'todo_ongoing_item': todo_ongoing.item,
                    'holder': todo_ongoing.user.name,
                    'holder_id': todo_ongoing.user.id
                }
                if todo_ongoing_info in todo_ongoing_list:
                    continue
                todo_ongoing_list.append(todo_ongoing_info)
            for todo_done in board.todos_done:
                thanks_from_list = []
                for thanks_from in todo_done.thanks_from:
                    thanks_from_info = {
                        'user_id': thanks_from.user.id,
                        'user_name': thanks_from.user.name
                    }
                    if thanks_from in thanks_from_list:
                        continue
                    thanks_from_list.append(thanks_from_info)
                todo_done_info = {
                    'todo_done_id': todo_done.id,
                    'todo_done_item': todo_done.item,
                    'done_by': todo_done.user.name,
                    'thanks_from': thanks_from_list
                }
                if todo_done_info in todo_done_list:
                    continue
                todo_done_list.append(todo_done_info)
            for member in board.users:
                member_info = {
                    'member_id': member.id,
                    'member_name': member.name,
                    'member_thanks_received': member.thanks_received,
                    'member_todos_created_num': member.todos_created_num,
                    'member_todos_done_num': member.todos_done_num
                }
                if member_info in member_list:
                    continue
                member_list.append(member_info)
            for memo in board.memos:
                memo_info = {
                    'memo_id': memo.id,
                    'memo_title': memo.title,
                    'memo_content': memo.content,
                    'memo_last_changed_time': memo.last_changed_time,
                    'holder_id': memo.user.id,
                    'holder_name': memo.user.name
                }
                if memo_info in memo_list:
                    continue
                memo_list.append(memo_info)
            board_info = {
                'board_id': board.id,
                'board_name': board.name,
                'todos': todo_list,
                'todos_ongoing': todo_ongoing_list,
                'todos_done': todo_done_list,
                'members': member_list,
                'memos': memo_list
            }
            board_list.append(board_info)

        for thank_to in g.user.thanks_to:
            thank_info = {
                'item': thank_to.todo_done.item,
                'user': thank_to.todo_done.user.name
            }
            thanks_to_list.append(thank_info)

    except Exception as e:
        responseObject = {
                'status': 'fail',
                'message': 'token or database query error',
                'error': str(e),
                'token': g.token
        }
        return jsonify(responseObject), 500 

    return jsonify({"user_id":g.user.id, "user_name":g.user.name, "confirmed":g.user.confirmed, "thanks_received": g.user.thanks_received, "todos_created_num":g.user.todos_created_num, "todos_done_num":g.user.todos_done_num, "boards":board_list, "thanks_to":thanks_to_list, "token":g.token}), 200


