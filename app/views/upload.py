from .. import app, db, auth
from flask import request, jsonify, make_response, g, Blueprint
from ..models import Board, Upload
from ..sign import cos_multi_signature, cos_single_signature

upload = Blueprint('upload', __name__)

@upload.route('/', methods=['GET'])
@auth.login_required
def dispach_signature():
	sign = cos_multi_signature()
	responseObject = {
			'status': 'success',
			'token': g.token,
			'upload_auth': sign
		}
	return jsonify(responseObject), 200


@upload.route('/', methods=['POST'])
@auth.login_required
def add_file():
	g.board = None
	repa = ('board_id','file_path','access_url', 'file_name_in_board')
	if not request.json or not all(para in repa for para in request.json):
		responseObject = {
				'status': 'fail',
				'message': 'You need to give board_id, file_path, access_url, file_name_in_board',
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

	g.upload = Upload(file_path=request.json['file_path'], access_url=request.json['access_url'], file_name_in_board=request.json['file_name_in_board'])

	g.board.uploads.append(g.upload)
	db.session.commit()
	responseObject = {
			'status': 'success',
			'message': '(%s) has been uploaded to (%s)' % (g.upload.file_path, g.board.name),
			'token': g.token
		}
	return jsonify(responseObject), 201

@upload.route('/', methods=['DELETE'])
@auth.login_required
def delete_file():
	g.todo = None
	repa = ('board_id','file_path')
	if not request.json or not all(para in repa for para in request.json):
		responseObject = {
				'status': 'fail',
				'message': 'You need to give board_id, file_path',
				'token': g.token
			}
		return make_response(jsonify(responseObject)), 400
	g.upload = Upload.query.filter_by(file_path=request.json['file_path']).first()
	if g.upload == None:
		responseObject = {
				'status': 'fail',
				'message': 'No such file',
				'token': g.token
		}
		return jsonify(responseObject), 400

	db.session.delete(g.upload)
	db.session.commit()
	responseObject = {
				'status': 'success',
				'message': '(%s) has been deleted in API server' % (g.upload.file_path),
				'token': g.token,
				'delete_auto': cos_single_signature(request.json['file_path'])
			}
	return make_response(jsonify(responseObject)), 200