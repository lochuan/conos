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
    if 'user_email' and 'user_name' and 'user_id' in data[0]:
        g.user = User.query.filter_by(email=data[0]['user_email']).first()
        new_exp = int(data[1]['exp']) - int(time.time()) + 3600
        g.token = JWT_REFRESH(app.config['SECRET_KEY'], expires_in=new_exp, algorithm_name='HS256').dumps({'user_id': data[0]['user_id'], 'user_name': data[0]['user_name'], 'user_email': data[0]['user_email']})
        g.token = g.token.decode('utf-8')
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
	return jsonify({"boards": board_list, "token": g.token})

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
				'message': '%s has been added' % g.board.name,
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
				'message': '%s has been deleted' % g.board.name,
				'token': g.token
			}
	return make_response(jsonify(responseObject)), 200

@board.route('/', methods=['PUT'])
@auth.login_required
def update_board():
	g.board = None
	if not request.json or not 'board_id' and 'board_name' in request.json:
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
				'message': 'The board name have changed from %s to %s' % (old_name, g.board.name),
				'token': g.token
			}
	return make_response(jsonify(responseObject)), 400

@board.route('/member/<int:board_id>', methods=['GET'])
@auth.login_required
def send_members(board_id):
	g.board = None
	member_list = []
	g.board = Board.query.filter_by(id=board_id).first()
	if g.board == None:
		responseObject = {
				'status': 'fail',
				'message': 'The board does not exist',
				'token': g.token
			}
		return jsonify(responseObject), 400
	for member in g.board.users:
		member_info = {
			'id': member.id,
			'name': member.name,
			'thanks': member.thanks_received
		}
		member_list.append(member_info)
	return jsonify({"members": member_list, "token": g.token}), 200

@board.route('/member/', methods=['POST'])
@auth.login_required
def add_member():
	g.board = None
	if not request.json or not 'board_id' and 'user_email' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'You need to give board_id and user_email',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	try:
		g.board = Board.query.filter_by(id=request.json['board_id']).first()
		g.user = User.query.filter_by(email=request.json['user_email']).first()
	except Exception as e:
		responseObject = {
				'status': 'fail',
				'message': 'database query error',
				'error': str(e),
				'token': g.token
		}
		return jsonify(responseObject), 500
	if g.user in g.board.users:
		responseObject = {
				'status': 'fail',
				'message': '%s already in the %s' % (g.user.name, g.board.name),
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	if g.user == None:
		responseObject = {
				'status': 'fail',
				'message': 'No such user_email',
				'token': g.token
		}
		return jsonify(responseObject), 400
	else:
		g.board.users.append(g.user)
		db.session.commit()
		responseObject = {
				'status': 'success',
				'message': '%s added in the %s' % (g.user.name, g.board.name),
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 201


@board.route('/member/', methods=['DELETE'])
@auth.login_required
def delete_member():
	g.board = None
	if not request.json or not 'board_id' and 'user_email' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'You need to give board_id and user_email',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	try:
		g.board = Board.query.filter_by(id=request.json['board_id']).first()
		g.user = User.query.filter_by(email=request.json['user_email']).first()
	except Exception as e:
		responseObject = {
				'status': 'fail',
				'message': 'database query error',
				'error': str(e),
				'token': g.token
		}
		return jsonify(responseObject), 500
	if g.user not in g.board.users:
		responseObject = {
				'status': 'fail',
				'message': '%s not in the %s' % (g.user.name, g.board.name),
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	else:
		g.board.users.remove(g.user)
		db.session.commit()
		responseObject = {
				'status': 'success',
				'message': '%s deleted from the %s' % (g.user.name, g.board.name),
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 200
