from .. import app, db, auth
from flask import request, jsonify, make_response, g, Blueprint
from ..models import Board, Meetup_Times
from datetime import datetime
import time

meetup = Blueprint('meetup', __name__)

@meetup.route('/', methods=['POST'])
@auth.login_required
def add_meetup():
	g.meetup = None
	g.board = None
	repa = ('board_id', 'start_time', 'end_time','location')
	if not request.json or not all(para in repa for para in request.json):
		responseObject = {
				'status': 'fail',
				'message': 'You need to give board_id, location, start_time and end_time',
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

	if g.board.meetup_status == 0:
		g.meetup = Meetup_Times(user_id=g.user.id, board_id=g.board.id, start_time=datetime.strptime(request.json['start_time'], '%Y-%m-%d %H:%M:%S'), end_time=datetime.strptime(request.json['end_time'], '%Y-%m-%d %H:%M:%S'))
		g.board.meetup_times.append(g.meetup)
		g.user.meetup_times.append(g.meetup)
		g.board.meetup_status = 1
		if g.board.meetup_location == None:
			g.board.meetup_location = request.json['location']
		db.session.commit()
		responseObject = {
			'status': 'success',
			'message': 'Meetup has been added in (%s)' % g.board.name,
			'token': g.token
		}
		return jsonify(responseObject), 200

	if len(g.user.meetup_times.all()) != 0:
		for mt in g.user.meetup_times:
			if mt.board.id == g.board.id:
				if request.json['location'] != 'null':
					g.board.meetup_location = request.json['location']
				mt.start_time = datetime.strptime(request.json['start_time'], '%Y-%m-%d %H:%M:%S')
				mt.end_time = datetime.strptime(request.json['end_time'], '%Y-%m-%d %H:%M:%S')
				db.session.commit
				match = check_match()
				if match:
					responseObject = {
						'status': 'success',
						'message': 'Your meetup has been updated',
						'token': g.token,
						'auto_match': match
					}
					return jsonify(responseObject), 200
				responseObject = {
						'status': 'success',
						'message': 'Your meetup has been updated',
						'token': g.token,
					}
				return jsonify(responseObject), 200
			else:
				g.meetup = Meetup_Times(user_id=g.user.id, board_id=g.board.id, start_time=datetime.strptime(request.json['start_time'], '%Y-%m-%d %H:%M:%S'), end_time=datetime.strptime(request.json['end_time'], '%Y-%m-%d %H:%M:%S'))
				g.board.meetup_times.append(g.meetup)
				g.user.meetup_times.append(g.meetup)
				g.board.meetup_status = 1
				if g.board.meetup_location == None:
					g.board.meetup_location = request.json['location']
				db.session.commit()
				match = check_match()
				if match:
					responseObject = {
						'status': 'success',
						'message': 'Meetup has been added in (%s)' % g.board.name,
						'token': g.token,
						'auto_match': match
					}
					return jsonify(responseObject), 200
				responseObject = {
						'status': 'success',
						'message': 'Meetup has been added in (%s)' % g.board.name,
						'token': g.token,
					}
				return jsonify(responseObject), 200
	else:
		g.meetup = Meetup_Times(user_id=g.user.id, board_id=g.board.id, start_time=datetime.strptime(request.json['start_time'], '%Y-%m-%d %H:%M:%S'), end_time=datetime.strptime(request.json['end_time'], '%Y-%m-%d %H:%M:%S'))
		g.board.meetup_times.append(g.meetup)
		g.user.meetup_times.append(g.meetup)
		g.board.meetup_status = 1
		if g.board.meetup_location == None:
			g.board.meetup_location = request.json['location']
		db.session.commit()
		match = check_match()
		if match:
			responseObject = {
				'status': 'success',
				'message': 'Meetup has been added in (%s)' % g.board.name,
				'token': g.token,
				'auto_match': match
			}
			return jsonify(responseObject), 200
		responseObject = {
				'status': 'success',
				'message': 'Meetup has been added in (%s)' % g.board.name,
				'token': g.token
			}
		return jsonify(responseObject), 200

	
@meetup.route('/', methods=['DELETE'])
@auth.login_required
def delete_meetup():
	g.board = None
	repa = ('board_id')
	if not request.json or not all(para in repa for para in request.json):
		responseObject = {
				'status': 'fail',
				'message': 'You need to give board_id',
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

	for meetup_time in g.board.meetup_times:
		db.session.delete(meetup_time)

	g.board.meetup_status = 0
	g.board.meetup_location = None
	g.board.meetup_time = None
	db.session.commit()
	responseObject = {
			'status': 'success',
			'message': 'Meetup has been removed from (%s)' % g.board.name,
			'token': g.token
		}
	return jsonify(responseObject), 200


def check_match():
	if len(g.board.users.all()) == len(g.board.meetup_times.all()):
		user_start_time={}
		user_end_time={}
		for meetup_time in g.board.meetup_times:
			user_start_time[meetup_time.user.name] = time.mktime(meetup_time.start_time.timetuple())
			user_end_time[meetup_time.user.name] = time.mktime(meetup_time.end_time.timetuple())

		v_start = user_start_time.values()
		k_start = user_start_time.keys()
		v_end = user_end_time.values()
		k_end = user_end_time.keys()

		if max(v_start) > min(v_end):
			g.board.meetup_status = 1
			g.board.meetup_time = None
			db.session.commit()
			responseObject = {
				'status': 'fail',
				'message': 'The start time of (%s) was too late, or the end time of (%s) was too early' % (k_start[v_start.index(max(v_start))], k_end[v_end.index(min(v_end))]),
			}
			return responseObject
		else:
			g.board.meetup_status = 2
			g.board.meetup_time = datetime.fromtimestamp(max(v_start))
			db.session.commit()
			responseObject = {
				'status': 'success',
				'message': 'Meet location:%s, Meet time: %s' % (g.board.meetup_location, g.board.meetup_time),
			}
			return responseObject
	else:
		return False