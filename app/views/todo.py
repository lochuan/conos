import time
from .. import app, db, auth, jwt_lt
from flask import request, jsonify, make_response, g, Blueprint
from itsdangerous import TimedJSONWebSignatureSerializer as JWT_REFRESH
from ..models import Todo, Todo_Ongoing, Todo_Done, Board, User, Thanks
from datetime import datetime

todo = Blueprint('todo', __name__)

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

@todo.route('/<int:board_id>', methods=['GET'])
@auth.login_required
def send_todos(board_id):
	g.board = None
	todo_list = []
	todo_ongoing_list = []
	todo_done_list = []
	g.board = Board.query.filter_by(id=board_id).first()
	if g.board == None:
		responseObject = {
				'status': 'fail',
				'message': 'The board does not exist',
				'token': g.token
			}
		return jsonify(responseObject), 400
	for todo in g.board.todos:
		todo_info = {
			'id': todo.id,
			'item': todo.item,
			'created_time': todo.created_time,
			'last_changed_time': todo.last_changed_time,
			'creator': todo.user.name
		}
		todo_list.append(todo_info)
	for todo_ongoing in g.board.todos_ongoing:
		todo_ongoing_info = {
			'id': todo_ongoing.id,
			'item': todo_ongoing.item,
			'created_time': todo_ongoing.created_time,
			'creator': todo_ongoing.user.name
		}
		todo_ongoing_list.append(todo_ongoing_info)
	for todo_done in g.board.todos_done:
		todo_done_info = {
			'id': todo_done.id,
			'item': todo_done.item,
			'created_time': todo_done.created_time,
			'creator': todo_done.user.name
		}
		todo_done_list.append(todo_done_info)
	return jsonify({'todos': todo_list, 'todos_ongoing': todo_ongoing_list, 'todos_done': todo_done_list}), 200

@todo.route('/', methods=['POST'])
@auth.login_required
def add_todo():
	g.board = None
	g.todo = None
	if not request.json or not 'board_id' and 'item' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'You need to give item, todo_type, board_id',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400

	g.board = Board.query.filter_by(id=request.json['board_id']).first()
	if g.board == None:
		responseObject = {
				'status': 'fail',
				'message': 'The board does not exist',
				'token': g.token
			}
		return jsonify(responseObject), 400

	g.todo = Todo(item=request.json['item'])
	g.board.todos.append(g.todo)
	g.user.todos.append(g.todo)
	db.session.commit()
	responseObject = {
			'status': 'success',
			'message': '%s has been added %s to %s' % (g.user.name, g.todo.item, g.board.name),
			'token': g.token
		}
	return jsonify(responseObject), 201
	

@todo.route('/', methods=['DELETE'])
@auth.login_required
def delete_todo():
	g.todo = None
	if not request.json or not 'todo_id' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'You need to give todo_id',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	g.todo = Todo.query.filter_by(id=request.json['todo_id']).first()
	if g.todo == None:
		responseObject = {
				'status': 'fail',
				'message': 'No such todo_id',
				'token': g.token
		}
		return jsonify(responseObject), 400

	db.session.delete(g.todo)
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': '%s has been deleted' % (g.todo.item),
				'token': g.token
			}
	return make_response(jsonify(responseObject)), 200

@todo.route('/', methods=['PUT'])
@auth.login_required
def update_board():
	g.todo = None
	if not request.json or not 'todo_id' in request.json or not 'todo_item' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'You need to give todo_id and todo_item',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	try:
		g.todo = Todo.query.filter_by(id=request.json['todo_id']).first()
	except Exception as e:
		responseObject = {
				'status': 'fail',
				'message': 'database query error',
				'error': str(e),
				'token': g.token
		}
		return jsonify(responseObject), 500
	old_item = g.todo.item
	g.todo.item = request.json['todo_item']
	g.todo.last_changed_time = datetime.utcnow()
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': 'The todo has been changed from %s to %s' % (old_item, g.todo.item),
				'token': g.token
			}
	return make_response(jsonify(responseObject)), 400

@todo.route('/move_to_ongoing/', methods=['POST'])
@auth.login_required
def move_to_ongoing():
	g.todo_ongoing = None
	g.todo = None
	g.board = None
	if not request.json or not 'todo_id' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'You need to give todo_id',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	g.todo = Todo.query.filter_by(id=request.json['todo_id']).first()
	if g.todo == None:
		responseObject = {
				'status': 'fail',
				'message': 'No such todo_id',
				'token': g.token
			}
		return jsonify(responseObject), 400

	g.board = g.todo.board
	g.todo_item = g.todo.item
	g.todo_ongoing = Todo_Ongoing(item=g.todo_item)
	g.board.todos_ongoing.append(g.todo_ongoing)
	g.user.todos_ongoing.append(g.todo_ongoing)
	db.session.delete(g.todo)
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': '%s has been moved to ongoing' % g.todo.item,
				'token': g.token
			}
	return make_response(jsonify(responseObject)), 201

@todo.route('/move_to_done/', methods=['POST'])
@auth.login_required
def move_to_done():
	g.todo_done = None
	g.todo_ongoing = None
	g.board = None
	if not request.json or not 'todo_ongoing_id' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'You need to give todo_ongoing_id',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	g.todo_ongoing = Todo_Ongoing.query.filter_by(id=request.json['todo_ongoing_id']).first()
	if g.todo_ongoing == None:
		responseObject = {
				'status': 'fail',
				'message': 'No such todo_ongoing_id',
				'token': g.token
			}
		return jsonify(responseObject), 400

	g.board = g.todo_ongoing.board
	g.todo_ongoing_item = g.todo_ongoing.item
	g.todo_done = Todo_Done(item=g.todo_ongoing_item)
	g.board.todos_done.append(g.todo_done)
	g.user.todos_done.append(g.todo_done)
	db.session.delete(g.todo_ongoing)
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': '%s has been moved to done' % g.todo_ongoing.item,
				'token': g.token
			}
	return make_response(jsonify(responseObject)), 201

@todo.route('/thankyou/', methods=['POST'])
@auth.login_required
def thankyou():
	g.todo_done = None
	if not request.json or not 'todo_done_id' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'You need to give todo_done_id',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	for thank in g.user.thanks_to:
		if thank.done_id == int(request.json['todo_done_id']):
			responseObject = {
				'status': 'fail',
				'message': 'Only can give thank once',
				'token': g.token
			}
			return jsonify(responseObject), 400
	g.todo_done = Todo_Done.query.filter_by(id=request.json['todo_done_id']).first()
	if g.todo_done == None:
		responseObject = {
				'status': 'fail',
				'message': 'No such todo_done_id',
				'token': g.token
			}
		return jsonify(responseObject), 400
	g.todo_done.user.thanks_received += 1
	g.thanks = Thanks(done_id = g.todo_done.id)
	g.user.thanks_to.append(g.thanks)
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': '%s thanks to %s, for his/her hard working' % (g.user.name, g.todo_done.user.name),
				'token': g.token
			}
	return jsonify(responseObject), 200