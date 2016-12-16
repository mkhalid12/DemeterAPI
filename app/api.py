from models import *
from dao import *
from flask_login import LoginManager, login_user, current_user, login_required
from flask import Flask, jsonify, make_response, request, flash
from flask_mongoengine import MongoEngine
from datetime import datetime
from bson import ObjectId, json_util
import json

MONGODB_SETTINGS = {'DB': "demeter_api"}

app = Flask(__name__)
#app.config['MONGODB_SETTINGS'] = MONGODB_SETTINGS
app.config["MONGODB_DB"] = 'demeter_api'
connect(
    'demeter_api',
    username='larissaleite',
    password='chamos',
    host='mongodb://larissaleite:chamos@ds133378.mlab.com:33378/demeter_api',
    port=133378
)

db = MongoEngine(app)

dao = Dao()

#initializing flask's login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	print user_id
	return User.objects.filter(id=user_id).first()

@login_manager.unauthorized_handler
def unauthorized():
	return json.dumps({ "status": "401", "message" : "Unauthorized" }), 401

def status_200():
	return json.dumps({ "status": "200", "message" : "Success" }), 200

def status_400():
	return json.dumps({ "status": "400", "message" : "Invalid parameters" }), 400

def status_404():
	return json.dumps({ "status": "404", "message" : "Resource not found" }), 404

@app.route("/login", methods=['POST'])
def login():
	if "email" in request.json and "password" in request.json:
		try:
			email = request.json["email"]
			password = request.json["password"]

			user = dao.authenticate_user(email, password)
			login_user(user)
			return self.status_200()
		except:
			return self.status_404()
	else:
		return self.status_400()

@app.route('/users/create_profile', methods=['POST'])
@login_required
def create_user_profile():
	if all(keys in request.json for keys in ("age", "gender", "country", "city", "name", "email", "ingredients", "restrictions")):
		try:
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
		except:
			return self.status_400()
	else:
		return self.status_400()

@app.route('/users/<string:id>', methods=['GET'])
def get_user(id):
	if ObjectId.is_valid(id):
		user = dao.get_user(id)
		if user is None:
			return json.dumps({ "status": "404", "message" : "User not found" }), 404
		return jsonify ( { 'user' : user } )
	else:
		return self.status_400()

@app.route('/recipes', methods=['GET'])
def get_recipes():
	try:
		query_filter = ""

		if "city" in request.json:
			query_filter += "city='"+request.json['location']+"',"
		if "age_min" in request.json:
			query_filter += "age__gte="+str(request.json['age_min']) + ","
		if "age_max" in request.json:
			query_filter += "age__lte="+str(request.json['age_max']) + ","

		query_filter = query_filter[:-1]

		recipes = dao.get_recipes_by_user_filters(query_filter)
		return recipes
	except:
		return self.status_400()

@app.route('/ingredients', methods=['GET'])
def get_all_ingredients():
	all_ingredients = dao.get_all_ingredients()
	return jsonify( { 'ingredients': all_ingredients } )

@app.route('/recipes/<string:id>', methods=['GET'])
def get_recipe(id):
	if ObjectId.is_valid(id):
		recipe = dao.get_recipe(id)
		if recipe is None:
			return self.status_404()
		return jsonify ( { 'recipe' : recipe } )
	else:
		return self.status_400()

@app.route('/reviews', methods=['GET'])
def get_recipe_reviews():
	if recipe_id in request.json:
		recipe_id = request.json["recipe_id"]

		if ObjectId.is_valid(recipe_id):
			if method == 'GET':
				try:
					reviews = dao.get_recipe_reviews(recipe_id)
					return reviews
				except:
					return self.status_404()
		else:
			return self.status_400()
	else:
		return self.status_400()

@app.route('/reviews/add', methods=['POST'])
@login_required
def add_recipe_review():
	if recipe_id in request.json:
		recipe_id = request.json["recipe_id"]

		if method == 'POST':
				if "user_id" in request.json and "text" in request.json:
					user_id = request.json["user_id"]
					text = request.json["text"]

					if ObjectId.is_valid(user_id):
						try:
							dao.save_recipe_review(user_id, recipe_id, text)
							return self.status_200()
						except:
							return self.status_404()
					else:
						return self.status_400()
				else:
					return self.status_400()
		else:
			return self.status_400()
	else:
		return self.status_400()

@app.route('/reviews/delete', methods=['DELETE'])
@login_required
def delete_recipe_review():
	if recipe_id in request.json:
		recipe_id = request.json["recipe_id"]

		if method == 'DELETE':
			if "review_id" in request.json:
				review_id = request.json["review_id"]
				if ObjectId.is_valid(review_id):
					try:
						dao.delete_recipe_review(recipe_id, review_id)
						return self.status_200()
					except:
						return self.status_404()
				else:
					return self.status_400()
			else:
				return self.status_400()
		else:
			return self.status_400()
	else:
		return self.status_400()

@app.route('/favorite_recipes', methods=['GET'])
def favorite_recipes():
	if "user_id" in request.json:
		user_id = request.json["user_id"]

		if ObjectId.is_valid(user_id):

			if method == 'GET':
				try:
					recipes = dao.get_user_favorite_recipes(user_id)
					return recipes
				except:
					return self.status_404()
		else:
			return self.status_400()
	else:
		return self.status_400()

@app.route('/favorite_recipes/add', methods=['POST'])
def add_favorite_recipes():
	if "user_id" in request.json:
		user_id = request.json["user_id"]

		if ObjectId.is_valid(user_id):

			if method == 'POST':
				if "recipe_id" in request.json:
					recipe_id = request.json["recipe_id"]

					if ObjectId.is_valid(user_id):
						try:
							dao.favorite_recipe(recipe_id, user_id)
							return self.status_200()
						except:
							return self.status_404()
					else:
						return self.status_400()
				else:
					return self.status_400()
		else:
			return self.status_400()
	else:
		return self.status_400()

@app.route('/favorite_recipes/delete', methods=['DELETE'])
def delete_favorite_recipes():
	if "user_id" in request.json:
		user_id = request.json["user_id"]

		if ObjectId.is_valid(user_id):

			if method == 'DELETE':
				if "recipe_id" in request.json:
					recipe_id = request.json["recipe_id"]

					if ObjectId.is_valid(recipe_id):
						try:
							dao.unfavorite_recipe(recipe_id, user_id)
							return self.status_200()
						except:
							return self.status_404()
					else:
						return self.status_400()
				else:
					return self.status_400()
		else:
			return self.status_400()
	else:
		return self.status_400()

@app.route('/ratings', methods=['GET'])
def get_user_ratings():
	if "user_id" in request.json:
		user_id = request.json["user_id"]
		if ObjectId.is_valid(user_id):
			try:
				ratings = dao.get_user_ratings(user_id)
				print ratings
				return jsonify ({ 'ratings' : json.loads(json_util.dumps(ratings)) })
			except:
				return self.status_404()
		else:
			return self.status_400()
	else:
		return self.status_400()

@app.route('/ratings', methods=['POST'])
@login_required
def new_user_ratings():
	if "recipe_id" in request.json and "user_id" in request.json and "rating" in request.json:

		user_id = request.json["user_id"]
		recipe_id = request.json["recipe_id"]
		rating = request.json["rating"]

		if ObjectId.is_valid(user_id) and ObjectId.is_valid(recipe_id):
			try:
				dao.save_user_recipe_rating(user_id, recipe_id, rating)
				return self.status_200()
			except:
				return self.status_404()
		else:
			return self.status_400()
	else:
		return self.status_400()

@app.route('/recommendations/recommend_recipes', methods=['GET'])
def recommend_recipes():
	if "recipe_id" in request.json:
		try:
			recipe_id = request.json["recipe_id"]

			recipes = json.loads(json_util.dumps(dao.get_similar_recipes(recipe_id)))
			return jsonify({ 'similar_recipes' : recipes })
		except:
			return self.status_400()
	else:
		return self.status_400()

@app.route('/recommendations/recommend_ingredient', methods=['GET'])
def recommend_ingredient():
	if "ingredient_name" in request.json:
		try:
			ingredient_name = request.json["ingredient_name"]

			ingredients = dao.get_similar_ingredients(ingredient_name)
			return jsonify ({ 'similar_recipes' : json.loads(json_util.dumps(ingredients)) })
		except:
			return self.status_400()
	else:
		return self.status_400()

if __name__ == '__main__':
	app.secret_key = 'secret key'
	from os import environ
	app.run(debug=False, host='0.0.0.0', port=int(environ.get("PORT", 5000)), processes=1)
