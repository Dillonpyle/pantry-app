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
			'id',
			required = True,
			help = "No id provided",
			location = ['form', 'json']
			)
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

	@marshal_with(recipe_fields)
	def put(self):
		args = self.reqparse.parse_args()
		print(args, 'hitting args in post request in RecipeEdit')

		## update recipe by args.id with 
		query = models.Recipe.update(**args).where(models.Recipe.id == args.id)
		query.execute()

		return (models.Recipe.get(models.Recipe.id == args.id), 200)





recipes_api = Blueprint('resources.recipes', __name__)
api = Api(recipes_api)

api.add_resource(
	RecipeList,
	'/recipes',
	endpoint="recipes"
	)

api.add_resource(
	RecipeEdit,
	'/recipe/edit',
	endpoint="recipes_edit"
	)
