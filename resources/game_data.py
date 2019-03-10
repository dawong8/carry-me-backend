import json
import requests



from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import check_password_hash


class Game(Resource):   #apex legends
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'username',
			required=True,
			help='no username provided',
			location=['form', 'json']
			)
		self.reqparse.add_argument(
			'platform',
			required=True,
			help='no platform provided',
			location=['form', 'json']
			)

		super().__init__()




	def post(self):
		args = self.reqparse.parse_args()
		r = requests.get('https://www.apexlegendshut.com/free-api?platform='+args['platform']+'&title='+args['username'])
		return r.json()


class Fortnite(Resource):
	def __init__(self): 
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'username',
			required=True,
			help='no username provided',
			location=['form', 'json']
			)
		self.reqparse.add_argument(
			'platform',
			required=True,
			help='no platform provided',
			location=['form', 'json']
			)

		super().__init__()

	def post(self): 
		args = self.reqparse.parse_args()
		params = {
			'TRN-Api-Key':'6e8ca0c1-3a89-4ff5-bd11-31f604949ae2'
			}
		r = requests.get('https://api.fortnitetracker.com/v1/profile/'+args['platform']+'/'+args['username'],headers=params )
		return r.json()		




game_api = Blueprint('resources.game_data', __name__)
api = Api(game_api)

api.add_resource(
    Game,
    '/game_data',
    endpoint='game'
)

api.add_resource(
	Fortnite,
	'/game_data/fortnite',
	endpoint='fortnite'
)
