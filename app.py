from flask import Flask, g, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_cors import CORS

from resources.users import users_api
from resources.ingredients import ingredients_api
from resources.pantry import pantry_api


import models
import forms
import config


DEBUG = config.DEBUG
PORT = config.PORT

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

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
CORS(ingredients_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(pantry_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users_api, origins=["http://localhost:3000"], supports_credentials=True)

app.register_blueprint(ingredients_api, url_prefix='/api/v1')
app.register_blueprint(pantry_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')


@app.route('/')
def index():
    return 'Pantry App'


if __name__ == '__main__':
    models.initialize()
    # try:
    #     models.User.create_user(
    #         username="test",
    #         password="asdf",
    #         )
    # except ValueError:
    #     ## pass is do nothing
    #     pass


    app.run(debug=DEBUG, port=PORT)





