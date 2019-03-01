import models
from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort

import models

recipe_fields = {
	'id': fields.Integer,
	'title': fields.String,
	'description': fields.String,
	'image_url': fields.String,
	'created_by': fields.String
}

class RecipeList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'title',
			required = True,
			help = "No title provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'description',
			required = True,
			help = "No description provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'image_url',
			required = False,
			help = "No image_url provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'created_by',
			required = True,
			help = "No username provided",
			location = ['form', 'json']
			)
		super().__init__()

## CREATE NEW RECIPE ============== WORKING
	@marshal_with(recipe_fields) 
	def post(self):
		args = self.reqparse.parse_args()
		print(args, 'hitting args in post request in RecipeList')
		recipe = models.Recipe.create(**args)
		return recipe


## SHOW ALL RECIPES =============== WORKING
	@marshal_with(recipe_fields)
	def get(self):
		recipes = [marshal(recipe, recipe_fields) for recipe in models.Recipe.select()]
		return recipes


class RecipeEdit(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'title',
			required = False,
			help = "No title provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'description',
			required = False,
			help = "No description provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'image_url',
			required = False,
			help = "No image_url provided",
			location = ['form', 'json']
			)

	## EDIT RECIPE -- Working, with userid check
	# @marshal_with(recipe_fields)
	def put(self, id, user_id):
		args = self.reqparse.parse_args()
		print(args, 'hitting args in put request in Recipe')

		## update recipe by args.id with 
		try:
			recipe_to_update = models.Recipe.get(models.Recipe.id == id and models.Recipe.created_by == user_id)
			query = models.Recipe.update(**args).where(models.Recipe.id == id)
			query.execute()
			return (marshal(models.Recipe.get(models.Recipe.id == id), recipe_fields), 200)
		except models.Recipe.DoesNotExist:
			return 'recipe does not exist or user does not have access'

	## DELETE RECIPE -- working
	def delete(self, id, user_id):
		try:
			recipe_to_delete = models.Recipe.get(models.Recipe.id == id and models.Recipe.created_by == user_id)
			query = models.Recipe.delete().where(models.Recipe.id == id)
			query.execute()
			return "recipe deleted"
		except models.Recipe.DoesNotExist:
			return 'Recipe does not exist or user does not have access'


## Show one Recipe by id ---- working
class Recipe(Resource):
	def get(self, id):
		try:
			recipe = models.Recipe.get(models.Recipe.id == id)
			return marshal(recipe, recipe_fields)
		except models.Recipe.DoesNotExist:
			return 'recipe does not exist'



recipes_api = Blueprint('resources.recipes', __name__)
api = Api(recipes_api)

api.add_resource(
	RecipeList,
	'/recipes',
	endpoint="recipes"
	)

api.add_resource(
	Recipe,
	'/recipe/<int:id>',
	endpoint="recipe"
	)

api.add_resource(
	RecipeEdit,
	'/recipe/<int:id>/<int:user_id>',
	endpoint="recipe_edit"
	)






