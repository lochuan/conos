from .. import app, db, auth, jwt_lt
from ..models import Board, User
from flask import request, jsonify, make_response, g, Blueprint

member = Blueprint('member', __name__)

@member.route('/', methods=['POST'])
@auth.login_required
def add_member():
	g.board = None
	repa = ('board_id', 'user_email')
	if not request.json or not all(para in repa for para in request.json):
		responseObject = {
				'status': 'fail',
				'message': 'You need to give board_id and user_email',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	try:
		g.board = Board.query.filter_by(id=request.json['board_id']).first()
		g.add_user = User.query.filter_by(email=request.json['user_email']).first()
	except Exception as e:
		responseObject = {
				'status': 'fail',
				'message': 'database query error',
				'error': str(e),
				'token': g.token
		}
		return jsonify(responseObject), 500
	if g.add_user in g.board.users:
		responseObject = {
				'status': 'fail',
				'message': '(%s) already in the (%s)' % (g.add_user.name, g.board.name),
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	if g.add_user == None:
		responseObject = {
				'status': 'fail',
				'message': 'No such user_email',
				'token': g.token
		}
		return jsonify(responseObject), 400
	else:
		g.board.users.append(g.add_user)
		db.session.commit()
		responseObject = {
				'status': 'success',
				'message': '(%s) has been added in the (%s)' % (g.add_user.name, g.board.name),
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 201


@member.route('/', methods=['DELETE'])
@auth.login_required
def delete_member():
	g.board = None
	repa = ('board_id', 'user_email')
	if not request.json or not all(para in repa for para in request.json):
		responseObject = {
				'status': 'fail',
				'message': 'You need to give board_id and user_email',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	try:
		g.board = Board.query.filter_by(id=request.json['board_id']).first()
		g.del_user = User.query.filter_by(email=request.json['user_email']).first()
	except Exception as e:
		responseObject = {
				'status': 'fail',
				'message': 'database query error',
				'error': str(e),
				'token': g.token
		}
		return jsonify(responseObject), 500
	if g.del_user not in g.board.users:
		responseObject = {
				'status': 'fail',
				'message': '(%s) not in the (%s)' % (g.del_user.name, g.board.name),
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	else:
		g.board.users.remove(g.del_user)
		db.session.commit()
		responseObject = {
				'status': 'success',
				'message': '(%s) deleted from the (%s)' % (g.del_user.name, g.board.name),
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 200