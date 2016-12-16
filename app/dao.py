from models import *

class Dao:

	# USER
	def authenticate_user(self, email, password):
		user = User.objects.filter(email=email).first()
		return user

	def get_user(self, user_id):
		user = User.objects.filter(id=user_id).first()

		if user is not None:
			favorite_recipes = []

			for recipe in user.favorite_recipes:
				favorite_recipes.append("https://guarded-mesa-45511.herokuapp.com/recipes/"+str(recipe.id))

			preferred_ingredients = []
			restricted_ingredients = []

			for ingredient in user.preferred_ingredients:
				preferred_ingredients.append(ingredient['name'])

			for ingredient in user.restricted_ingredients:
				restricted_ingredients.append(ingredient['name'])

			user = {
				'age' : user.age,
				'gender' : user.gender,
				'city' : user.city,
				'country' : user.country,
				'preferred_ingredients' : preferred_ingredients,
				'restricted_ingredients' : restricted_ingredients,
				'favorite_recipes' : favorite_recipes
			}

		return user

	def create_user(self, name, email, age, gender, city, country, ingredients, restrictions):
		ingredient_restrictions = []
		preferred_ingredients = []

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

		user = User(
			city=city,
			country=country,
			email=email,
			name=name,
			age=age,
			gender=gender,
			preferred_ingredients=preferred_ingredients,
			restricted_ingredients=restricted_ingredients
		)

		user.save()

	def favorite_recipe(self, recipe_id, user_id):
		user = User.objects.filter(id=user_id).first()
		recipe = Recipe.objects.filter(id=str(recipe_id)).first()

		user.update(add_to_set__favorite_recipes=recipe)

	def unfavorite_recipe(self, recipe_id, user_id):
		user = User.objects.filter(id=user_id).first()
		recipe = Recipe.objects.filter(id=str(recipe_id)).first()

		user.update(pull__favorite_recipes=recipe)

	def get_user_favorite_recipes(self, user_id):
		user = User.objects.filter(id=str(user_id)).first()
		_user_favorite_recipes = user.favorite_recipes

		user_favorite_recipes = []

		#try to do it direct in the query, to get only the ids
		for recipe in _user_favorite_recipes:
			if str(recipe.id) not in user_favorite_recipes:
				user_favorite_recipes.append(str(recipe.id))

		return user_favorite_recipes

	# RATING
	def get_recipe_ratings(self, recipe_id):
		recipe = Recipe.objects.filter(id=str(recipe_id)).first()
		ratings = Rating.objects.filter(recipe=recipe)

		return ratings

	def get_user_ratings(self, user_id):
		user = User.objects.filter(id=str(user_id)).first()
		ratings = Rating.objects.filter(user=user)

		return ratings

	def save_user_recipe_rating(self, user_id, recipe_id, rating):
		user = User.objects.filter(id=user_id).first()
		recipe = Recipe.objects.filter(id=str(recipe_id)).first()

		user_recipe_rate = Rating.objects(user=user, recipe=recipe).first()

		#checks if rating already exists
		if user_recipe_rate is None:

			user_recipe_rate = Rating(
				user=user,
				recipe=recipe,
				rating=rating
			)

			user_recipe_rate.save()
		else:
			user_recipe_rate.update(set__rating=rating)

	# RECIPE
	def get_recipe(self, recipe_id):
		recipe = Recipe.objects.filter(id=str(recipe_id)).first()

		if recipe is not None:
			ingredients = []

			for ingredient in recipe['ingredients']:
				ingredients.append(ingredient['full_text'])

			reviews = []

			for review in recipe.reviews:
				user = self.get_user(review.user.id)
				reviews.append({ 'text' : review.text, 'user' : user, 'date' : review.date })

			ratings = []
			for rating in Rating.objects.filter(recipe=recipe).only("rating"):
				ratings.append(rating.rating)

			recipe = {
				#'id' : recipe_id,
				'title' : recipe['title'],
				'img' : recipe['image'],
				'instructions' : recipe['instructions'],
				'labels' : recipe['labels'],
				'ingredients' : ingredients,
				'reviews' : reviews,
				'ratings' : ratings
			}

		return recipe

	def get_similar_recipes(self, recipe_id):
		_similar_recipes = Recipe.objects(id=str(recipe_id)).only("similar_recipes").first().similar_recipes
		similar_recipes = []

		for recipe in _similar_recipes:
			similar_recipes.append(self.get_recipe(recipe.id))

		return similar_recipes

	def get_recipe_reviews(self, recipe_id):
		recipe = Recipe.objects.filter(id=str(recipe_id)).first()

		reviews = recipe.reviews

		_reviews = []
		for review in reviews:
			_reviews.append({ 'id':review.id, 'text':review.text, 'user_fb_id':review.user.fb_id, 'user_id':str(review.user.id) , 'date':str(review.date) })
		return _reviews

	def save_recipe_review(self, user_id, recipe_id, text):
		user = User.objects.filter(id=user_id).first()

		review_id = ObjectId()

		review = Review(
			id = str(review_id),
			user = user,
			text = text
		)

		recipe = Recipe.objects.filter(id=str(recipe_id)).first()

		recipe.reviews.append(review)
		recipe.save()

		_reviews = []
		_reviews.append({ 'id':review.id, 'text':review.text, 'user_fb_id':review.user.fb_id, 'user_id':str(review.user.id) , 'date':str(review.date) })

	def delete_recipe_review(self, recipe_id, review_id):
		return Recipe.objects(id=str(recipe_id)).update(pull__reviews__id=str(review_id))

	def get_recipes_by_user_filters(self, filters):
		favorite_recipes = User.objects(filters).only(favorite_recipes).as_pymongo()
		recipes = []

		for recipe in favorite_recipes:
			recipes.append(self.get_recipe(recipe.id))
		return recipes

	# INGREDIENTS
	def get_all_ingredients(self):
		return Recipe.objects.distinct(field="ingredients.name")

	def get_similar_ingredients(self, ingredient_name):
		similar_ingredients = SimilarIngredient.objects(name=ingredient_name).scalar("similar_ingredients")
		return similar_ingredients
