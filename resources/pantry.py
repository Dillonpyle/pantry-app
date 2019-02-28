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
	except models.pantry.DoesNotExist:
		## this sends our 404 response for us
		abort(404)
	else: 
		return pantry

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

	## create new pantry entry -- not working
	@marshal_with(pantry_fields)
	def post(self):
		args = self.reqparse.parse_args()
		print(args, '-- args in post request in pantry api')

		## check db to see if pantry item with user_id and ingredient_id already exists
		try:
			pantry_entry = models.Pantry.get(models.Pantry.user_id == args.user_id and models.Pantry.ingredient_id == args.ingredient_id )
			print(pantry_entry, 'this is pantry_entry')
			# query = models.Pantry.update(pantry_entry.quantity = pantry_entry.quantity + 1).where(models.Dog.id==id)
			# ## we have to execute the update query
			# query.execute()
			## increase pantry_entry quantity by 1
			## return pantry_entry


			return 'pantry_entry found'

		except models.Pantry.DoesNotExist:
			## if it doesn't create pantry item
			print(args, '-- args after quantity has been defined')
			print(args["ingredient_id"], 'this is ingredient id')
			pantry_entry = models.Pantry.create(
				ingredient_id=args["ingredient_id"],
				user_id=args["user_id"],
				quantity=1
			)
			# pantry_entry.save()
			pantry_1 = models.Pantry.get(models.Pantry.id == 1)
			print(pantry_1.__dict__)

			# return [marshal(pantry_entry, pantry_fields)]
			return pantry_1
		# else: 
		# 	## if it does increase quantity by 1
		# 	return 'pantry item must increase by 1'

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





