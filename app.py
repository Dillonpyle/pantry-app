from flask import Flask

import models

DEBUG = True
PORT = 8000

app = Flask(__name__)



@app.route('/')
def hello_world():
	return 'Pantry App'

if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT)