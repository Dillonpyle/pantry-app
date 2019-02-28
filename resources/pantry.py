from flask import jsonify, Blueprint, abort

from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_required

import models

pantry_fields = {
	'ingredient_id': fields.Integer,
	'user_id': fields.Integer,
	# 'quantity': fields.Integer,
	# 'created_at': fields.DateTime,
}

## function that finds 
def pantry_or_404_id(user_id):
	try:
		pantry = models.Pantry.select().where(models.Pantry.user_id == user_id)
	except models.pantry.DoesNotExist:
		## this sends our 404 response for us
		abort(404)
	else: 
		return pantry

class PantryList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required = True,
			help = "No pantry name provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'type',
			required = True,
			help = "No pantry type provided",
			location = ['form', 'json']
			)
		super().__init__()

	## Get all pantry entries -- untested
	def get(self):
		pantry = [marshal(pantry, pantry_fields) for pantry in models.Pantry.select()]
		return {'pantry': pantry}

	## create new pantry entry -- not working
	# @marshal_with(pantry_fields)
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hitting args in post request in ingredients api')
		print(args.user_id)
		print(type(args.ing_id))
		print(args, '-- args in post request in pantry api')
		# pantry = models.Pantry.create(**args)
		# return pantry
		return 'hitting post route'

class Pantry(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required = False,
			help = "no pantry name provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'type',
			required = False,
			help = "No pantry type provided",
			location = ['form', 'json']
			)

	## Show route -- untested
	@marshal_with(pantry_fields)
	def get(self, user_id):
		return pantry_or_404_id(user_id)
    ## define a function to find our pantry or send our 404		

  ## Update route -- untested
	@marshal_with(pantry_fields)
	def put(self, id):
		args = self.reqparse.parse_args()
		query = models.Pantry.update(**args).where(models.Pantry.id==id)
		query.execute()
		return (models.Pantry.get(models.Pantry.id==id), 200)

	## delete route -- untested
	def delete(self, id):
		query = models.Pantry.delete().where(models.Pantry.id==id)
		query.execute()
		return "pantry was deleted"


pantry_api = Blueprint('resources.pantry', __name__)
api = Api(pantry_api)

api.add_resource(
	PantryList,
	'/pantry_items',
	endpoint="pantries"
	)





