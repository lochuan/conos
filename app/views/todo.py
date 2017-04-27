from .. import app, db, auth
from flask import request, jsonify, make_response, g, Blueprint
from ..models import Todo, Todo_Ongoing, Todo_Done, Board, Thanks
from datetime import datetime

todo = Blueprint('todo', __name__)

@todo.route('/', methods=['POST'])
@auth.login_required
def add_todo():
	g.board = None
	g.todo = None
	repa = ('board_id','item')
	if not request.json or not all(para in repa for para in request.json):
		responseObject = {
				'status': 'fail',
				'message': 'You need to give item, board_id',
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
	g.user.todos_created_num += 1
	db.session.commit()
	responseObject = {
			'status': 'success',
			'message': '(%s) has been added (%s) to (%s)' % (g.user.name, g.todo.item, g.board.name),
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
				'message': '(%s) has been deleted' % (g.todo.item),
				'token': g.token
			}
	return make_response(jsonify(responseObject)), 200

@todo.route('/', methods=['PUT'])
@auth.login_required
def update_todo():
	g.todo = None
	repa = ('todo_id','todo_item')
	if not request.json or not all(para in repa for para in request.json):
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
	if g.todo == None:
		responseObject = {
				'status': 'fail',
				'message': 'No such todo_id',
				'token': g.token
		}
		return jsonify(responseObject), 400
	old_item = g.todo.item
	g.todo.item = request.json['todo_item']
	g.todo.last_changed_time = datetime.utcnow()
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': 'The todo has been changed from (%s) to (%s)' % (old_item, g.todo.item),
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
				'message': '(%s) has been moved to ongoing' % g.todo.item,
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
	if g.todo_ongoing not in g.user.todos_ongoing:
		responseObject = {
			'status': 'fail',
			'message': 'This todo_ongoing does not belong to you',
			'token': g.token
		}
		return jsonify(responseObject), 400
	g.board = g.todo_ongoing.board
	g.todo_ongoing_item = g.todo_ongoing.item
	g.todo_done = Todo_Done(item=g.todo_ongoing_item)
	g.board.todos_done.append(g.todo_done)
	g.user.todos_done.append(g.todo_done)
	g.user.todos_done_num += 1
	db.session.delete(g.todo_ongoing)
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': '(%s) has been moved to done' % g.todo_ongoing.item,
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
	g.todo_done.thanks_received += 1
	g.todo_done.user.thanks_received += 1
	g.thanks = Thanks(done_id = g.todo_done.id, user_id = g.user.id)
	g.user.thanks_to.append(g.thanks)
	g.todo_done.thanks_from.append(g.thanks)
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': '(%s) thanks to (%s), for his/her hard working' % (g.user.name, g.todo_done.user.name),
				'token': g.token
			}
	return jsonify(responseObject), 200