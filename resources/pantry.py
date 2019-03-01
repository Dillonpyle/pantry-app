from flask import jsonify, Blueprint, abort

from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_required

import models

pantry_fields = {
	'ingredient_id': fields.String,
	'user_id': fields.String,
	'quantity': fields.String,
	'created_at': fields.DateTime,
}
					# ingredient_id: ing_id,
					# user_id: this.props.user.user_id


## function that finds 
def pantry_or_404_id(user_id):
	try:
		pantry = models.Pantry.select().where(models.Pantry.user_id == user_id)
		return pantry
	except models.pantry.DoesNotExist:
		## this sends our 404 response for us
		abort(404)

class PantryList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'ingredient_id',
			required = True,
			help = "No ingredient_id provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'user_id',
			required = True,
			help = "No user_id provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'quantity',
			required = False,
			help = "No quantity provided",
			location = ['form', 'json']
			)
		super().__init__()

	## Get all pantry entries -- untested
	def get(self):
		pantry = [marshal(pantry, pantry_fields) for pantry in models.Pantry.select()]
		return {'pantry': pantry}

	## create new pantry entry -- Working
	@marshal_with(pantry_fields)
	def post(self):
		args = self.reqparse.parse_args()
		print(args, '-- args in post request in pantry api')
		## check db to see if pantry item with user_id and ingredient_id already exists
		try:

			## find pantry entry matching user_id and ingredient_id
			pantry_entry = models.Pantry.get(models.Pantry.user_id == args.user_id and models.Pantry.ingredient_id == args.ingredient_id )
			print(pantry_entry.__dict__, 'this is pantry_entry')
			
			## increase pantry_entry quantity by 1
			pantry_entry.quantity += 1
			pantry_entry.save()
			print(pantry_entry.__dict__, 'this is pantry_entry with increased quantity')
			return pantry_entry

		## if it doesn't create pantry item
		except models.Pantry.DoesNotExist:
			print(args, '-- args after quantity has been defined')
			print(args["ingredient_id"], 'this is ingredient id')
			pantry_entry = models.Pantry.create(
				ingredient_id=args["ingredient_id"],
				user_id=args["user_id"],
				quantity=1
			)
			pantry_entry.save()
			# pantry_1 = models.Pantry.get(models.Pantry.user_id == args.user_id and models.Pantry.ingredient_id == args.ingredient_id )
			# print(pantry_1.__dict__)
			print(pantry_entry.__dict__)

			# return [marshal(pantry_entry, pantry_fields)]
			return pantry_entry
		# else: 
		# 	## if it does increase quantity by 1
		# 	return 'pantry item must increase by 1'

class Pantry(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'user_id',
			required = True,
			help = "no user_id provided",
			location = ['form', 'json']
			)



	## Display all pantry Items of User ============================= Look here dummy
	# @marshal_with(pantry_fields)
	def post(self):
		try:
			args = self.reqparse.parse_args()
			print(args, 'these are args')
			print(args.user_id, 'this is args.user_id')
			users_pantry = models.Pantry.select().where(models.Pantry.user_id == args.user_id)
			print(users_pantry.__dict__)
			return [marshal(pantry, pantry_fields) for pantry in users_pantry]
		except Exception as e:
			return 'pantry does not exist'
    ## define a function to find our pantry or send our 404		

## ===================================================================



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

api.add_resource(
	Pantry,
	'/pantry',
	endpoint="pantry"
	)



