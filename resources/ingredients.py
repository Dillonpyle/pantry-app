from flask import jsonify, Blueprint, abort

from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_required

import models

ingredient_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'type': fields.String
}

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

ingredients_api = Blueprint('resources.ingredients', __name__)
api = Api(ingredients_api)

api.add_resource(
	IngredientList,
	'/ingredients',
	endpoint="ingredients"
	)









