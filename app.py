from flask import Flask, g, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_cors import CORS

from resources.users import users_api
from resources.ingredients import ingredients_api
from resources.recipes import recipes_api
from resources.pantry import pantry_api
from resources.ingredient_in_recipe import ingredient_in_recipe_api


import models
import os

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = "af;ljlwenncv__lnwecvjkso"

login_manager = LoginManager()

# sets up our login for the app
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


# set up cors
CORS(ingredients_api, origins=["https://dillonpantryfe.herokuapp.com", "http://localhost:3000"], supports_credentials=True)
CORS(ingredient_in_recipe_api, origins=["https://dillonpantryfe.herokuapp.com", "http://localhost:3000"], supports_credentials=True)
CORS(recipes_api, origins=["https://dillonpantryfe.herokuapp.com", "http://localhost:3000"], supports_credentials=True)
CORS(pantry_api, origins=["https://dillonpantryfe.herokuapp.com", "http://localhost:3000"], supports_credentials=True)
CORS(users_api, origins=["https://dillonpantryfe.herokuapp.com", "http://localhost:3000"], supports_credentials=True)


app.register_blueprint(ingredients_api, url_prefix='/api/v1')
app.register_blueprint(ingredient_in_recipe_api, url_prefix='/api/v1')
app.register_blueprint(recipes_api, url_prefix='/api/v1')
app.register_blueprint(pantry_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')


@app.route('/')
def index():
    return 'Pantry App'

if 'HEROKU' in os.environ:
    print('hitting ')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
