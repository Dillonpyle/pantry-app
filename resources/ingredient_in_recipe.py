from flask import jsonify, Blueprint, abort

from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask_login import login_required

import models

## format to what i want to return to react
ingredient_in_recipe_fields = {
	'recipe_id': fields.String,
	'ingredient_id': fields.String,
	'amount': fields.String,
	'unit': fields.String
}




# Show all ingredients in recipe -- UNTESTED, add some ingredients to a recipe
# need recipe id
class RecipeIngredientList(Resource):
	def get(self, r_id):
		try:
			recipe_ingredinets = [marshal(list_item, ingredient_in_recipe_fields) for list_item in models.IngredientInRecipe.select().where(models.IngredientInRecipe.recipe_id == r_id)]
			return recipe_ingredients

			## MIGHT STILL NEED THIS
			# recipe_ingredients = models.IngredientInRecipe.get(models.IngredientInRecipe.id == id)
			# return marshal(recipe_ingredients, ingredient_in_recipe_fields)
		except models.IngredientInRecipe.DoesNotExist:
			return 'ingredients in recipe do not exist does not exist'

		# dogs = [marshal(dog, dog_fields) for dog in models.Dog.select()]




class RecipeIngredient(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'amount',
			required = True,
			help = "no user_id provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'unit',
			required = True,
			help = "no user_id provided",
			location = ['form', 'json']
			)
		# super().__init__()

# # Add ingredient to recipe
# # need user id and recipe id ### NEEDS USER AUTH
	@marshal_with(ingredient_in_recipe_fields)
	def post(self, r_id, i_id):
		args = self.reqparse.parse_args()
		print(args, 'hitting args in post route in ingedient_in_recipe')
		try:
			## check db to see if ingredientInRecipe already exists
			ing_in_recipe = models.IngredientInRecipe.get(models.IngredientInRecipe.recipe_id == r_id and models.IngredientInRecipe.ingredient_id == i_id )
			return ing_in_recipe

		except models.IngredientInRecipe.DoesNotExist:
			ing_in_recipe = models.IngredientInRecipe.create(
				recipe_id=r_id,
				ingredient_id=i_id,
				amount=args["amount"],
				unit=args["unit"]
			)
			ing_in_recipe.save()
			print(ing_in_recipe, 'this is ing_in_recipe that was created')
			return ing_in_recipe



class RecipeIngredientEdit(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'amount',
			required = True,
			help = "no user_id provided",
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'unit',
			required = True,
			help = "no user_id provided",
			location = ['form', 'json']
			)

	# # Remove ingredient from recipe
	# # need user id and recipe id
	# def delete(self, r_id, i_id, u_id):
		# check if user created recipe
		# select r of r_id where created_by == u_id
		## if user did create recipe
		### delete ri where r_id == r_id and i_id == i_id
		## if user didn't create recipe tell them to fuck off




# # Edit amount or unit of ingredients in recipe
# # need user id and recipe id





ingredient_in_recipe_api = Blueprint('resources.ingredient_in_recipe', __name__)
api = Api(ingredient_in_recipe_api)

api.add_resource(
	RecipeIngredientList,
	'/recipe_ingredient/list/<int:r_id>',
	endpoint="recipe_ingredient_list"
	)

api.add_resource(
	RecipeIngredient,
	'/recipe_ingredient/<int:r_id>/<int:i_id>',
	endpoint="recipe_ingredient"
	)

api.add_resource(
	RecipeIngredient,
	'/recipe_ingredient/edit/<int:r_id>/<int:i_id>/<int:u_id>',
	endpoint="recipe_ingredient_edit"
	)

