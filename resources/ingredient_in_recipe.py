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

# # Add ingredient to recipe
# # need user id and recipe id
	def post(self, r_id, i_id):
		args = self.reqparse.parse_args()
		print(args, 'hitting args in post request in dog api')

		return 'hey there pal'


	# ## create new pantry entry -- Working
	# @marshal_with(pantry_fields)
	# def post(self):
	# 	args = self.reqparse.parse_args()
	# 	print(args, '-- args in post request in pantry api')
	# 	## check db to see if pantry item with user_id and ingredient_id already exists
	# 	try:

	# 		## find pantry entry matching user_id and ingredient_id
	# 		pantry_entry = models.Pantry.get(models.Pantry.user_id == args.user_id and models.Pantry.ingredient_id == args.ingredient_id )
	# 		print(pantry_entry.__dict__, 'this is pantry_entry')
			
	# 		## increase pantry_entry quantity by 1
	# 		pantry_entry.quantity += 1
	# 		pantry_entry.save()
	# 		print(pantry_entry.__dict__, 'this is pantry_entry with increased quantity')
	# 		return pantry_entry

	# 	## if it doesn't create pantry item
	# 	except models.Pantry.DoesNotExist:
	# 		print(args, '-- args after quantity has been defined')
	# 		print(args["ingredient_id"], 'this is ingredient id')
	# 		pantry_entry = models.Pantry.create(
	# 			ingredient_id=args["ingredient_id"],
	# 			user_id=args["user_id"],
	# 			quantity=1
	# 		)
	# 		pantry_entry.save()
	# 		print(pantry_entry.__dict__)
	# 		return pantry_entry



# # Remove ingredient from recipe
# # need user id and recipe id

# # Edit amount or unit of ingredients in recipe
# # need user id and recipe id


ingredient_in_recipe_api = Blueprint('resources.ingredient_in_recipe', __name__)
api = Api(ingredient_in_recipe_api)

api.add_resource(
	RecipeIngredientList,
	'/recipe_ingredient_list/<int:r_id>',
	endpoint="recipe_ingredient_list"
	)

api.add_resource(
	RecipeIngredient,
	'/recipe_ingredient/<int:r_id>/<int:i_id>',
	endpoint="recipe_ingredient"
	)



