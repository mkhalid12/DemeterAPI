from app import app
from config import APP_STATIC

from flask import Flask, render_template, jsonify, make_response, request, flash
from flask_login import login_user, current_user, login_required
from app.models import *
from datetime import datetime

@app.route('/', methods = ['GET'])
def index():
	if current_user.is_authenticated:
		return home()
	return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	if request.method == 'GET':
		return render_template('profile.html', user=current_user)
	else:
		return home()

@app.route('/register', methods=['POST'])
def register():
	age = request.json['age']
	gender = request.json['gender']
	location = request.json['location']
	restrictions = request.json['restrictions']
	ingredients = request.json['ingredients']

	preferred_ingredients = []
	ingredient_restrictions = []

	for ingredient_name in ingredients:
		ingredient = Ingredient(
			name = ingredient_name
		)
		preferred_ingredients.append(ingredient)

	for ingredient_name in restrictions:
		ingredient = Ingredient(
			name = ingredient_name
		)
		ingredient_restrictions.append(ingredient)

	user = User.objects.filter(id=current_user.id).first()

	user.update(**{
		'set__age' : age,
		'set__gender': gender,
		'set__location' : location,
		'set__preferred_ingredients':preferred_ingredients,
		'set__allergies':ingredient_restrictions
	})

	return home()


@app.route('/home', methods=['GET'])
@login_required
def home():

	all_recipes = Recipe.objects[:10]

	recipes = []

	for recipe in all_recipes:
		ingredients = []

		for ingredient in recipe['ingredients']:
			ingredients.append({
				'text' : ingredient['full_text']
			})

		recipes.append({
			'title' : recipe['title'],
			'img' : recipe['image'],
			'instructions' : recipe['instructions'],
			'vegetarian' : recipe['vegetarian'],
			'glutenFree' : recipe['glutenFree'],
			'dairyFree' : recipe['dairyFree'],
			'fatFree' : recipe['fatFree'],
			'peanutFree' : recipe['peanutFree'],
			'calories' : recipe['calories'],
			'ingredients' : ingredients
		})

	return render_template("home.html", recipes=recipes)

@app.route('/api/user', methods=['GET'])
def get_user():
	user = User.objects.filter(id=current_user.id).first()

	user = {
		'age' : user.age,
		'gender' : user.gender,
		'location' : user.location,
		'ingredients' : user.preferred_ingredients,
		'restrictions' : user.allergies
	};

	return jsonify(user=user)

@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
	all_ingredients = Recipe.objects.distinct(field="ingredients.name")

	return jsonify( { 'all_ingredients': all_ingredients } )

@app.route('/template_select', methods = ['GET'])
def get_template_select():
	return render_template('template_select.html')
