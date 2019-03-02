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

# >>> query = User.select()
# >>> [user.username for user in query]
# ['Charlie', 'Huey', 'Peewee']

# >>> query[1]
# <__main__.User at 0x7f83e80f5550>

# >>> query[1].username
# 'Huey'

# >>> query[:2]
# [<__main__.User at 0x7f83e80f53a8>, <__main__.User at 0x7f83e80f5550>]

#### NONE OF THIS BULLSHIT WORKS ============================================

# class AllIngredientsInRecipes(Resource):
# 	def get(self):
# 		try:
# 			query = models.IngredientInRecipe.selcet()
# 			ingredient_in_recipe = [ingredient for ingredient in query]



# # Show all ingredients in recipe -- UNTESTED, add some ingredients to a recipe
# # need recipe id
# class RecipeIngredientList(Resource):
# 	def get(self, r_id):
# 		try:
# 			## query is not working... make it work
# 			query = models.IngredientInRecipe.select().where(models.IngredientInRecipe.recipe_id == r_id)
# 			recipe_ingredinets = [ingredient.unit for ingredient in query]

# 			# recipe_ingredinets = [marshal(list_item, ingredient_in_recipe_fields) for list_item in models.IngredientInRecipe.select().where(models.IngredientInRecipe.recipe_id == r_id)]

# 			print(recipe_ingredients)
# 			return recipe_ingredients


# 			## MIGHT STILL NEED THIS
# 			# recipe_ingredients = models.IngredientInRecipe.get(models.IngredientInRecipe.id == id)
# 			# return marshal(recipe_ingredients, ingredient_in_recipe_fields)
# 		except models.IngredientInRecipe.DoesNotExist:
# 			return 'ingredients in recipe do not exist does not exist'

# 		# dogs = [marshal(dog, dog_fields) for dog in models.Dog.select()]

## function that finds ingredients of recipe
def i_in_r_or_404_id(recipe_id):
	try:
		ingredients = models.IngredientInRecipe.select().where(models.IngredientInRecipe.recipe_id == recipe_id)
		return ingredients
	except models.IngredientInRecipe.DoesNotExist:
		## this sends our 404 response for us
		abort(404)

class RecipeIngredientList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'recipe_id',
			required = True,
			help = "no user_id provided",
			location = ['form', 'json']
			)

	## Display all Ingredients In Recipe ============================= NOT WORKING
	# @marshal_with(pantry_fields)
	def post(self):
		try:
			args = self.reqparse.parse_args()
			print(args, 'these are args')
			print(args.recipe_id, 'this is args.recipe_id')
			ingredients_in_recipe = i_in_r_or_404_id(args.recipe_id)
			return [marshal(ingredient, ingredient_in_recipe_fields) for ingredient in ingredients_in_recipe]
			# return "it'll be ok"
		except Exception as e:
			print(e)
			return "there was an error"


## ===================================================================




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
## rewrite to inclue u_id
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
	def delete(self, r_id, i_id, u_id):
		try:
			# check if user created recipe
			models.Recipe.select().where(models.Recipe.created_by == u_id and models.Recipe.id == r_id)
			## if user did create recipe
			### delete ri where r_id == r_id and i_id == i_id
			query = models.IngredientInRecipe.delete().where(models.IngredientInRecipe.recipe_id == r_id and models.IngredientInRecipe.ingredient_id == i_id)
			query.execute()
			return "ingredient in recipe deleted"
		except models.Recipe.DoesNotExist:
			## if user didn't create recipe tell them to fuck off
			return "user does not have permission or recipe does not exist"





# # Edit amount or unit of ingredients in recipe
# # need user id and recipe id





ingredient_in_recipe_api = Blueprint('resources.ingredient_in_recipe', __name__)
api = Api(ingredient_in_recipe_api)

api.add_resource(
	RecipeIngredientList,
	'/recipe_ingredient/list',
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

