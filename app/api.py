from models import *
#from flask_login import login_user, current_user, login_required
from flask import Flask, jsonify, make_response, request, flash
from datetime import datetime
from bson import ObjectId, json_util

MONGODB_SETTINGS = {'DB': "demeter_api"}
app = Flask(__name__)

#authentication
@app.route('/users/', methods=['POST'])

@app.route('/users/<int:id>', methods=['GET'])

@app.route('/recipes', methods=['GET'])

@app.route('/ingredients', methods=['GET'])

@app.route('/recipes/<int:id>', methods=['GET'])

#authentication except for GET
@app.route('/recipes/reviews', methods=['GET', 'POST', 'DELETE'])
#recipe_id in the body/query

#authentication except for GET
@app.route('/favorite_recipes/', methods=['GET', 'POST', 'DELETE'])
#user_id and recipe_id in the body/query

#authentication only for POST
@app.route('/ratings', methods=['GET', 'POST'])

@app.route('/recommendations/recommend_recipe', methods=['GET'])
#recipe_id in the body/query

@app.route('/recommendations/recommend_ingredient', methods=['GET'])
#ingredient name in the body/query

if __name__ == '__main__':
	app.secret_key = 'secret key'
	from os import environ
	app.run(debug=True, host='0.0.0.0', port=int(environ.get("PORT", 5000)), processes=1)
