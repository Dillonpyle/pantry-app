from flask import jsonify, Blueprint, abort

from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_required

import models

ingredient_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'type': fields.String
}

def ingredient_or_404(ingredient_id):
	try:
		ingredient = models.Ingredient.get(models.Ingredient.id == ingredient_id)
	except models.Ingredient.DoesNotExist:
		## this sends our 404 response for us
		abort(404)
	else: 
		return ingredient

class IngredientList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required = True,
			help = "No ingredient name provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'type',
			required = True,
			help = "No ingredient type provided",
			location = ['form', 'json']
			)
		super().__init__()

	## ingredients index route
	def get(self):
		ingredients = [marshal(ingredient, ingredient_fields) for ingredient in models.Ingredient.select()]
		return {'ingredients': ingredients}

	## create route
	@marshal_with(ingredient_fields)
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hitting args in post request in ingredients api')
		ingredient = models.Ingredient.create(**args)
		return ingredient

class Ingredient(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required = False,
			help = "No ingredient name provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'type',
			required = False,
			help = "No ingredient type provided",
			location = ['form', 'json']
			)

	## Show route -- working
	@marshal_with(ingredient_fields)
	def get(self, id):
		return ingredient_or_404(id)
    ## define a function to find our ingredient or send our 404		

  ## Update route -- NOT working
	@marshal_with(ingredient_fields)
	def put(self, id):
		args = self.reqparse.parse_args()
		query = models.Ingredient.update(**args).where(models.Ingredient.id==id)
		query.execute()
		return (models.Ingredient.get(models.Ingredient.id==id), 200)

	## delete route -- working
	def delete(self, id):
		query = models.Ingredient.delete().where(models.Ingredient.id==id)
		query.execute()
		return "Ingredient was deleted"




ingredients_api = Blueprint('resources.ingredients', __name__)
api = Api(ingredients_api)

api.add_resource(
	IngredientList,
	'/ingredients',
	endpoint="ingredients"
	)

api.add_resource(
	Ingredient,
	'/ingredients/<int:id>',
	endpoint='ingredient'
	)








