from .. import app, db, auth
from ..models import Board, Memo
from flask import request, jsonify, make_response, g, Blueprint
from datetime import datetime

memo = Blueprint('memo', __name__)

@memo.route('/', methods=['POST'])
@auth.login_required
def add_memo():
	g.board = None
	repa = ('board_id', 'title', 'content')
	if not request.json or not all(para in repa for para in request.json):
		responseObject = {
				'status': 'fail',
				'message': 'You need to give board_id, title and content',
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

	g.memo = Memo(title=request.json['title'], content=request.json['content'])
	g.board.memos.append(g.memo)
	g.user.memos.append(g.memo)
	g.user.memos_created_num += 1
	db.session.commit()
	responseObject = {
			'status': 'success',
			'message': '(%s) has been added (%s) to (%s)' % (g.user.name, g.memo.title, g.board.name),
			'token': g.token
		}
	return jsonify(responseObject), 201


@memo.route('/', methods=['DELETE'])
@auth.login_required
def delete_memo():
	g.todo = None
	if not request.json or not 'memo_id' in request.json:
		responseObject = {
				'status': 'fail',
				'message': 'You need to give memo_id',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	g.memo = Memo.query.filter_by(id=request.json['memo_id']).first()
	if g.memo == None:
		responseObject = {
				'status': 'fail',
				'message': 'No such memo_id',
				'token': g.token
		}
		return jsonify(responseObject), 400

	db.session.delete(g.memo)
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': '(%s) has been deleted' % (g.memo.title),
				'token': g.token
			}
	return make_response(jsonify(responseObject)), 200

@memo.route('/', methods=['PUT'])
@auth.login_required
def update_memo():
	g.memo = None
	repa = ('memo_id','title', 'content')
	if not request.json or not all(para in repa for para in request.json):
		responseObject = {
				'status': 'fail',
				'message': 'You need to give memo_id, title and content',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	try:
		g.memo = Memo.query.filter_by(id=request.json['memo_id']).first()
	except Exception as e:
		responseObject = {
				'status': 'fail',
				'message': 'database query error',
				'error': str(e),
				'token': g.token
		}
		return jsonify(responseObject), 500
	if g.memo == None:
		responseObject = {
				'status': 'fail',
				'message': 'No such memo_id',
				'token': g.token
		}
		return jsonify(responseObject), 400
	old_title = g.memo.title
	g.memo.title = request.json['title']
	g.memo.content = request.json['content']
	g.memo.last_changed_time = datetime.utcnow()
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': 'The (%s) has been changed' % old_title,
				'token': g.token
			}
	return make_response(jsonify(responseObject)), 400