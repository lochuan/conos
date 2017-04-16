from .. import db, auth, jwt
from ..models import Board, User
from flask import request, jsonify, make_response, g, Blueprint

board = Blueprint('board', __name__)

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

@board.route('/', methods=['GET'])
@auth.login_required
def send_boards():
	board_list = []
	for board in g.user.boards:
		board_info = {
			'id': board.id,
			'name': board.name,
			'created_time': board.created_time
		}
		board_list.append(board_info)
	return str(board_list), 200

@board.route('/', methods=['POST'])
@auth.login_required
def add_board():
	g.board = None
	if not request.json or not 'board_name' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'You need to give board a name'
			}
		return make_response(jsonify(responseObject)), 400
	g.board = Board(name=request.json['board_name'])
	g.board.users.append(g.user)
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': '%s has been added' % g.board.name
			}
	return make_response(jsonify(responseObject)), 200

@board.route('/', methods=['DELETE'])
@auth.login_required
def delete_board():
	g.board = None
	if not request.json or not 'board_id' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'You need to give board a name'
			}
		return make_response(jsonify(responseObject)), 400
	g.board = Board.query.filter_by(id=request.json['board_id']).first()
	db.session.delete(g.board)
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': '%s has been deleted' % g.board.name
			}
	return make_response(jsonify(responseObject)), 200

@board.route('/', methods=['PUT'])
@auth.login_required
def update_board():
	g.board = None
	if not request.json or not 'board_id' and 'board_name' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'You need to give board a name'
			}
		return make_response(jsonify(responseObject)), 400
	g.board = Board.query.filter_by(id=request.json['board_id']).first()
	g.board.name = request.json['board_name']
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': 'You changed board name to %s' % g.board.name
			}
	return make_response(jsonify(responseObject)), 400