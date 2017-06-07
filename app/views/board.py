import time
from .. import app, db, auth, jwt_lt
from ..models import Board, User
from flask import request, jsonify, make_response, g, Blueprint
from itsdangerous import TimedJSONWebSignatureSerializer as JWT_REFRESH

board = Blueprint('board', __name__)

@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = jwt_lt.loads(token, return_header=True)
    except:
        return False
    repa = ('user_email', 'user_name', 'user_id')
    if all(para in repa for para in data[0]):
        g.user = User.query.filter_by(email=data[0]['user_email']).first()
        new_exp = int(data[1]['exp']) - int(time.time()) + 3600
        g.token = JWT_REFRESH(app.config['SECRET_KEY'], expires_in=new_exp, algorithm_name='HS256').dumps({'user_id': data[0]['user_id'], 'user_name': data[0]['user_name'], 'user_email': data[0]['user_email']})
        g.token = g.token.decode('utf-8')
        return True
    return False

@board.route('/', methods=['POST'])
@auth.login_required
def add_board():
    g.board = None
    if not request.json or not 'board_name' in request.json:
        responseObject = {
                'status': 'fail',
                'message': 'You need to give board a name',
                'token': g.token
            }
        return make_response(jsonify(responseObject)), 400
    g.board = Board(name=request.json['board_name'])
    g.board.users.append(g.user)
    db.session.commit()
    responseObject = {
                'status': 'success',
                'message': '(%s) has been added' % g.board.name,
                'token': g.token
            }
    return make_response(jsonify(responseObject)), 201

@board.route('/', methods=['DELETE'])
@auth.login_required
def delete_board():
    g.board = None
    if not request.json or not 'board_id' in request.json:
        responseObject = {
                'status': 'fail',
                'message': 'You need to give board a name',
                'token': g.token
            }
        return make_response(jsonify(responseObject)), 400
    g.board = Board.query.filter_by(id=request.json['board_id']).first()
    if g.board == None:
        responseObject = {
                'status': 'fail',
                'message': 'No such board_id',
                'token': g.token
        }
        return jsonify(responseObject), 400
    db.session.delete(g.board)
    db.session.commit()
    responseObject = {
                'status': 'success',
                'message': '(%s) has been deleted' % g.board.name,
                'token': g.token
            }
    return make_response(jsonify(responseObject)), 200

@board.route('/', methods=['PUT'])
@auth.login_required
def update_board():
    g.board = None
    repa = ('board_id','board_name')
    if not request.json or not all(para in repa for para in request.json):
        responseObject = {
                'status': 'fail',
                'message': 'You need to give board a name',
                'token': g.token
            }
        return make_response(jsonify(responseObject)), 400
    try:
        g.board = Board.query.filter_by(id=request.json['board_id']).first()
    except Exception as e:
        responseObject = {
                'status': 'fail',
                'message': 'database query error',
                'error': str(e),
                'token': g.token
        }
        return jsonify(responseObject), 500
    old_name = g.board.name
    g.board.name = request.json['board_name']
    db.session.commit()
    responseObject = {
                'status': 'success',
                'message': 'The board name have changed from (%s) to (%s)' % (old_name, g.board.name),
                'token': g.token
            }
    return make_response(jsonify(responseObject)), 400

@board.route('/<board_id>/', methods=['GET'])
def get_board_info(board_id):
    g.board = None
    g.board = Board.query.filter_by(id=board_id).first()
    if g.board == None:
        responseObject = {
                'status': 'fail',
                'message': 'No such board_id',
                'token': g.token
        }
        return jsonify(responseObject), 400

    todo_list = []
    todo_ongoing_list = []
    todo_done_list = []
    member_list = []
    memo_list = []
    meetup_list = []
    file_list = []

    for todo in g.board.todos:
        todo_info = {
            'todo_id':todo.id,
            'todo_item': todo.item,
            'todo_last_changed_time': todo.last_changed_time,
            'creator': todo.user.name
        }
        todo_list.append(todo_info)
    for todo_ongoing in g.board.todos_ongoing:
        todo_ongoing_info = {
            'todo_ongoing_id': todo_ongoing.id,
            'todo_ongoing_item': todo_ongoing.item,
            'holder': todo_ongoing.user.name,
            'holder_id': todo_ongoing.user.id
        }
        todo_ongoing_list.append(todo_ongoing_info)
    for todo_done in g.board.todos_done:
        thanks_from_list = []
        for thanks_from in todo_done.thanks_from:
            thanks_from_info = {
                'user_id': thanks_from.user.id,
                'user_name': thanks_from.user.name
            }
            thanks_from_list.append(thanks_from_info)
        todo_done_info = {
            'todo_done_id': todo_done.id,
            'todo_done_item': todo_done.item,
            'done_by': todo_done.user.name,
            'thanks_from': thanks_from_list
        }
        todo_done_list.append(todo_done_info)
    for member in g.board.users:
        member_info = {
            'member_id': member.id,
            'member_name': member.name,
            'member_thanks_received': member.thanks_received,
            'member_todos_ongoing_num:': member.todos_ongoing.count(),
            'member_todos_created_num': member.todos_created_num,
            'member_todos_done_num': member.todos_done_num
        }
        member_list.append(member_info)
    for memo in g.board.memos:
        memo_info = {
            'memo_id': memo.id,
            'memo_title': memo.title,
            'memo_content': memo.content,
            'memo_last_changed_time': memo.last_changed_time,
            'holder_id': memo.user.id,
            'holder_name': memo.user.name
        }
        memo_list.append(memo_info)
    for upload in g.board.uploads:
        file_info = {
            'file_name':upload.file_name_in_board,
            'access_url': upload.access_url,
            'file_path': upload.file_path
        }
        file_list.append(file_info)
    for meetup in g.board.meetup_times:
        meetup_info = {
            'user': meetup.user.name,
            'user_id': meetup.user.id,
            'start_time': meetup.start_time,
            'end_time': meetup.end_time
        }
        meetup_list.append(meetup_info)

    board_info = {
                'board_id': g.board.id,
                'board_name': g.board.name,
                'todos': todo_list,
                'todos_ongoing': todo_ongoing_list,
                'todos_done': todo_done_list,
                'members': member_list,
                'memos': memo_list,
                'files': file_list,
                'meetup_status': g.board.meetup_status,
                'meetup_location': g.board.meetup_location,
                'meetup_time': g.board.meetup_time,
                'meetup_user_responses': meetup_list
        }
    resp = make_response(jsonify(board_info))
    resp.headers['access-control-allow-origin'] = '*'
    return resp

