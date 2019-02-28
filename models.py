import datetime
from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

DATABASE = SqliteDatabase('mypantry.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, password):
        try:
            cls.select().where(
                (cls.username == username)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            raise Exception("User with email or username already exists")


class Ingredient(Model):
    name = TextField(default=None)
    type = TextField(default=None)

    class Meta:
        database = DATABASE


class Recipe(Model):
    title = CharField()
    image_url = CharField()
    source_url = CharField()
    publisher = CharField()
    publisher_url = CharField()
    social_rank = CharField()
    created_by = ForeignKeyField(User)

    class Meta:
        database = DATABASE

# Ingredient of User


class Pantry(Model):
    ingredient_id = ForeignKeyField(Ingredient)
    user_id = ForeignKeyField(User)
    quantity = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class IngredientInRecipe(Model):
    recipe_id = ForeignKeyField(Recipe)
    ingredient_id = ForeignKeyField(Ingredient)

    class Meta:
        database = DATABASE


class RecipeOfUser(Model):
    user_id = ForeignKeyField(User)
    recipe_id = ForeignKeyField(Recipe)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables(
        [User, Ingredient, Recipe, Pantry, IngredientInRecipe, RecipeOfUser], safe=True)
    DATABASE.close()
