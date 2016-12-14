import datetime
from flask_login import UserMixin
from mongoengine import *

class Ingredient(EmbeddedDocument):
	name = StringField(max_length=255, required=True)
	meta = {'allow_inheritance': True}

#not necessary to inherit EmbeddedDocument again since Ingredient already does
class ExtendedIngredient(Ingredient):
	full_text = StringField(max_length=500)
	amount = IntField()
	unit = StringField(max_length=25)

class Review(EmbeddedDocument):
	id = StringField(max_length=500, required=True)
	text = StringField(max_length=500, required=True)
	user = ReferenceField('User')
	recipe = ReferenceField('Recipe')
	date = DateTimeField(default=datetime.datetime.now, required=True)

class Rating(Document):
	user = ReferenceField('User')
	recipe = ReferenceField('Recipe')
	rating = IntField(required=True)

class Recipe(Document):
	title = StringField(max_length=255, required=True)
	ingredients = ListField(EmbeddedDocumentField('ExtendedIngredient'))
	image = StringField(max_length=255)
	instructions = StringField(max_length=500)
	labels = ListField(StringField(max_length=100))
	reviews = ListField(EmbeddedDocumentField('Review'))

class User(Document, UserMixin):
	name = StringField(max_length=255, required=True)
	age = IntField()
	gender = BinaryField()
	email = StringField(max_length=255)
	city = StringField(max_length=255)
	country = StringField(max_length=255)
	preferred_ingredients = ListField(EmbeddedDocumentField('Ingredient'))
	restricted_ingredients = ListField(EmbeddedDocumentField('Ingredient'))
	favorite_recipes = ListField(ReferenceField('Recipe'))
