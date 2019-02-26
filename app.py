from flask import Flask
from flask_cors import CORS

## Import resources
from resources.ingredients import ingredients_api

## Import Models
import models

DEBUG = True
PORT = 8000

app = Flask(__name__)

## set up cors
CORS(ingredients_api, origin=["http://localhost:3000"], supports_credentials=True)

app.register_blueprint(ingredients_api, url_prefix='/api/v1')


@app.route('/')
def hello_world():
	return 'Pantry App'

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)