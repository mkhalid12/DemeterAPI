from models import *
from dao import *
#from flask_login import login_user, current_user, login_required
from flask import Flask, jsonify, make_response, request, flash
from flask_mongoengine import MongoEngine
from datetime import datetime
from bson import ObjectId, json_util
import json

MONGODB_SETTINGS = {'DB': "demeter_api"}

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = MONGODB_SETTINGS

db = MongoEngine(app)

dao = Dao()

#authentication
@app.route('/users/', methods=['POST'])
def add_user():
	age = request.json['age']
	gender = request.json['gender']
	country = request.json['country']
	city = request.json['city']
	restrictions = request.json['restrictions']
	ingredients = request.json['ingredients']
	name = request.json['name']
	email = request.json['email']

	user = dao.create_user(name, email, age, gender, city, country, ingredients, restrictions)

	return jsonify ( { 'user' : user } )

#keep recipes as links????
@app.route('/users/<string:id>', methods=['GET'])
def get_user(id):
	if ObjectId.is_valid(id):
		user = dao.get_user(id)
		if user is None:
			return json.dumps({ "status": "500", "message" : "User not found" }), 404
		return jsonify ( { 'user' : user } )
	else:
		return json.dumps({ "status": "400", "message" : "Invalid Parameter" }), 400

@app.route('/recipes', methods=['GET'])
def get_recipes():
# body parameters (change on swagger). how to put them optional??:
	location = request.json['location']
	age = request.json['age']
	ingredient = request.json['ingredient'] #put as many ingredients
	label = request.json['label']

	#query dao

@app.route('/ingredients', methods=['GET'])
def get_all_ingredients():
	all_ingredients = dao.get_all_ingredients()
	return jsonify( { 'ingredients': all_ingredients } )

@app.route('/recipes/<string:id>', methods=['GET'])
def get_recipe(id):
	if ObjectId.is_valid(id):
		recipe = dao.get_recipe(id)
		if recipe is None:
			return json.dumps({ "status": "500", "message" : "Recipe not found" }), 404
		return jsonify ( { 'recipe' : recipe } )
	else:
		return json.dumps({ "status": "400", "message" : "Invalid Parameter" }), 400

#authentication except for GET
@app.route('/recipes/reviews', methods=['GET', 'POST', 'DELETE'])
def recipe_reviews():
	recipe_id = request.json["recipe_id"]

	if ObjectId.is_valid(recipe_id):
		if method == 'GET':
			try:
				reviews = dao.get_recipe_reviews(recipe_id)
				return reviews
			except:
				return json.dumps({ "status": "400", "message" : "Recipe not found" }), 404

		elif method == 'POST':
			user_id = request.json["user_id"]
			text = request.json["text"]

			if ObjectId.is_valid(user_id):
				try:
					reviews = dao.save_recipe_review(user_id, recipe_id, text)
					return reviews
				except:
					return json.dumps({ "status": "400", "message" : "Recipe or User not found" }), 404
			else:
				return json.dumps({ "status": "400", "message" : "Invalid Parameters" }), 400

		elif method == 'DELETE':
			review_id = request.json["review_id"]
			if ObjectId.is_valid(review_id):
				try:
					dao.delete_recipe_review(recipe_id, review_id)
					return json.dumps({ "status": "200", "message" : "Success" }), 200
				except:
					return json.dumps({ "status": "400", "message" : "Recipe/review not found" }), 404
			else:
				return json.dumps({ "status": "400", "message" : "Invalid Parameters" }), 400
	else:
		return json.dumps({ "status": "400", "message" : "Invalid Parameter recipe_id" }), 400

#authentication except for GET
@app.route('/favorite_recipes/', methods=['GET', 'POST', 'DELETE'])
def favorite_recipes():
	user_id = request.json["user_id"]

	if method == 'GET':
		try:
			recipes = dao.get_user_favorite_recipes(user_id)
			return recipes
		except:
			return json.dumps({ "status": "400", "message" : "User not found" }), 404

	if method == 'POST':
		recipe_id = request.json["recipe_id"]

		if ObjectId.is_valid(user_id):
			try:
				recipes = dao.favorite_recipe(recipe_id, user_id)
				return recipes
			except:
				return json.dumps({ "status": "400", "message" : "Recipe or User not found" }), 404
		else:
			return json.dumps({ "status": "400", "message" : "Invalid Parameters" }), 400

	elif method == 'DELETE':
		recipe_id = request.json["recipe_id"]

		if ObjectId.is_valid(recipe_id):
			try:
				dao.unfavorite_recipe(recipe_id, user_id)
				return json.dumps({ "status": "200", "message" : "Success" }), 200
			except:
				return json.dumps({ "status": "400", "message" : "Recipe/user not found" }), 404
		else:
			return json.dumps({ "status": "400", "message" : "Invalid Parameters" }), 400


#authentication TODO change in swagger just for GET from user and put inside recipe as well
#@app.route('/ratings', methods=['POST'])
#def ratings():


@app.route('/recommendations/recommend_recipe', methods=['GET'])
def recommend_recipes():
	recipe_id = request.json["recipe_id"]

	recipes = dao.get_similar_recipes(recipe_id)
	return recipes

@app.route('/recommendations/recommend_ingredient', methods=['GET'])
def recommend_ingredient():
	ingredient_name = request.json["ingredient_name"]

	ingredients = dao.get_similar_ingredients(ingredient_name)
	return ingredients

if __name__ == '__main__':
	app.secret_key = 'secret key'
	from os import environ
	app.run(debug=False, host='0.0.0.0', port=int(environ.get("PORT", 5000)), processes=1)
